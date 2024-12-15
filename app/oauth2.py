from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


# SECRET_KEY
# Algorithm
# Expiration time # this sets that how long the user should be logged in.

# we dont need to hardcode this inour code, we can make it as environment variable.
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    # current time + add 30 mins
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# Function to verify the access token
def verify_access_token(token: str, credentials_exception):
    try:
        # decodes the token we will send while accessing something. 
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])  # decode the token
    
        # After decoding it will match the userid field, which we added in the payload while generating a payload for the user then it compares it.
        id: str = payload.get("user_id") # extract the id
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))  # Convert id to string
 # validate with a schema the tokne_data 
#  https://chatgpt.com/share/67534493-8370-8012-a710-1ef175400457
    except JWTError:
        raise credentials_exception
    
    return token_data

# Will be Passed as Dependency in any pathOperation
# It will take the token automatically from request, will extract the id, verify the token by calling verify_access_token, extract id and fetch the user from database, add
# this function actually returning user, and can modify as per ur need what u have to return.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first() # query to database to grab the user

    return user 