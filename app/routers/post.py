from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, utils, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List, Optional
from .. import oauth2

# we used route object to split up our route or path operations in different file and make them use in the one "main" file.  
router = APIRouter(
    prefix="/posts",    # as all out path operation using the "/posts" path endpoint, we can remover it from the path operation and add the path in this prefix to actually use it.
    # for "/posts/{id}" it going to be  /posts + /{id} = /posts/{id}

    tags=['Posts'] # It helps to categories the request and improve the readability of our documention.
)


# this function represents retriving all the post from social media
# we need to add decorator to turn function into special path operation fuction.
# Gets all the Posts

# @router.get("/", response_model=List[schemas.Post]) # to retrieve we going to this url.  

# @router.get("/") # to retrieve we going to this url.  

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # logic for retrieving posts - RAW SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # get posts using ORM or specifically SQL alchemy.
    # the filter will only retrieve the post of the user Logged in
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() 

    # {{URL}}posts?limit=2&skip=0&search=I%20am%20a%Hacker
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # query with Parameters.

    # {{URL}}posts?limit=2&skip=0&search=I%20am%20a%Hacker
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts

    # return results

    # posts = db.query(models.Post).filter(models.Post).all() # normal query
    # print(posts)
    # return posts


# fetching individual post by an ID.
# @router.get("/{id}", response_model=schemas.Post) # {id} - represents path parameter.

@router.get("/{id}", response_model=schemas.PostOut) 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # RAW - SQL
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    # query is fetching a tuple of (Post, votes) instead of a single Post object.
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # Extract post and votes
    post, votes = result

    # Check if the post belongs to the current user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actoin.")
    
    # Return the post along with votes
    return {"post": post, "votes": votes}

# Creating a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.email) # we getting back the user which is returned from "get_current_user" function.

    # Create new Post
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())    
    # add to the database 
    db.add(new_post)
    # commmited it
    db.commit()
    # retrive the new post and store it in new_post variable
    db.refresh(new_post)
    
    return new_post



# DELETING a Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # RAW - SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit() # to make`` changes in the database we have to commit it.
     
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # check if the post exists
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    # check the user deleting the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actoin.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATing Post
@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # RAW - SQL
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # setups the query to grab the specific post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grabs the specific post
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actoin.")
    
    # chained update method to it
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()

    return post_query.first() # send it back to the user
