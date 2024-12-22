# We can define all our fixtures here and any fixtures you define in this file will automatically accessible to any of our tests within this package test.py, even sub-packages.

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
from app.oauth2 import create_access_token
from app import models

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

@pytest.fixture
def test_user(client):
    user_data = {"email": "obama@gmail.com", "password": "password123"} 
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# didn't understand
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "First title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
        
    post_map = map(create_post_model, posts_data) 
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts