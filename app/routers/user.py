from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, utils, models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# USER Functionality - Creating a User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password


    # Convert the input Pydantic model into a dictionary using `model_dump` (Pydantic V2)
    new_user = models.User(**user.model_dump())  # Ensure the model has fields matching the User table
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the updated instance from the database
    
    
    return new_user

# Fetch User based on the id
@router.get("/{id}", response_model=schemas.Userout)
def get_user(id: int, db: Session = Depends(get_db), response_model=schemas.Userout):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exit")
    
    return user