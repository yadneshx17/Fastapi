from builtins import str
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# This Model defines the structor of the Request & Response 
# provide some validation to ensure that the body all the data field in the request match ups the model.
# Technically we dont need this but you want to be as stict as possbile when what kind of the data we recive

# These are schemas for how user would send us data within the Body of the request. and How in response we will return it again

# Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value to the field

class PostCreate(PostBase): # extends PostBase
    pass


# Response model for user creation
class Userout(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes  = True


# RESPONSE MODEL
class Post(PostBase):
    # other fileds are inherited from postbase
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout # returns the pydantic model info of the user.

    class Config:
        from_attributes  = True

class PostOut(BaseModel):
    Post: Post # post: Post
    votes: int

    class Config:
        from_attributes  = True

# User Creation Schemas.
class UserCreate(BaseModel):
    email: EmailStr # EmailStr - validates that its a email and not just normal text
    password: str
    
# Response model for user creation
class Userout(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes  = True

# UserLogin
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

# Validating the Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=2) # type: ignore # direction upvote (like) or downvote (dislike)