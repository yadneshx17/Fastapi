#  Testing Database Related Code

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Yadnesh%40017@localhost:5432/fastapi_test"

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test' 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


"""
@pytest.fixture
def client():
    # run our code before we run our test
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)
    
    # run our code after our code finisher
    Base.metadata.drop_all(bind=engine)
"""

# passing one fixture into another fixture

# return database object,
@pytest.fixture()
def session():
    
    # Create & destroy database after each test
    # he every time new tables banvel like mang equal key value wale error type errors yenar nhi
    Base.metadata.drop_all(bind=engine)  # drops all 
    Base.metadata.create_all(bind=engine) # create all 
    db = TestingSessionLocal()
    try:
        yield db  # Provide the session to the endpoint
    finally:
        db.close()


# returns client
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session  # Provide the session to the endpoint
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # tests all
