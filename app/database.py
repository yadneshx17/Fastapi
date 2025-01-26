from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# Hard Coded URL
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:Yadnesh%40017@localhost:5432/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

print(SQLALCHEMY_DATABASE_URL)

# makes an database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionmaker function creats SessionLocal class 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session to the endpoint
    finally:
        db.close()  # Ensure the session is closed


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password='Yadnesh@017', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection made successfully")
#         break
#     except Exception as error:
#         print("connection failed")
#         print("Error:", error)
#         time.sleep(2)
