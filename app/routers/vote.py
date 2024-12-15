from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # find the post if exist or not
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    # check if vote already existed
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() # stores the voted post if exist.   

    if(vote.dir == 1): # For Vote.
        # if vote found
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        # if not votted before it assigns the vote
        # sets the post_id and User_id combination.
        new_vote = models.Vote(post_id= vote.post_id, user_id=current_user.id)  
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    else: # For For Disvoting

        # first checks if the vote exist - only able to disvote if any exist there.
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        # if exist the voted post.
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": " successfully deleted Vote"}