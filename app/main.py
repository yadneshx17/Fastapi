from fastapi import Body, FastAPI
from fastapi.params import Body
from .database import engine, get_db 
from . import models
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_hostname)
print(settings.database_name)

# this commands told Sql alchemy to run the create statement so that it generated all of the tables when first started up. we don't need it now cause Alembic is    used.

# models.Base.metadata.create_all(bind=engine)
    
app = FastAPI() # instance of Fastapi 

# origins = ["https://www.google.com", "https://www.youtube.com"]
# Every One Can access it Every Single domain/Origin
origins = ["*"] 

app.add_middleware(
    CORSMiddleware, # function it will run for all the requests.
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],  # allow/restrict http methods through this
    allow_headers=["*"], 
)



# importing all the path operations from different files into one.
app.include_router(post.router) # we can also specify  (prefix="/posts") here
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")  # / - is the path that reference the path that we have to go in the url.
def root():
    return {"message": "welcome to my API !"} # whatever we return here is gonna be the data sent back to the user
