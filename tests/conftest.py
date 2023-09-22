import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app import models
#create a testing database

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


 # Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db #in testing we create a different sessiion for testing purposes

#Testing with simplest welcome


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind= engine)
    Base.metadata.create_all(bind= engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    #run code before running the test
    #run code afterward test code
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db #in testing we create a different sessiion for testing purposes
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test_user@user.com",
                 "password": "testing1"}
    
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "test_user2@user.com",
                 "password": "testing2"}
    
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user



@pytest.fixture
def token(test_user):
    
    return create_access_token({"user_id" : test_user['id']})
     


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user_2, session):
    posts_data = [{"title": "Bahamas trip"
         ,"content": "first_content"
         ,"owner_id": test_user['id']}
        ,{"title": "LA trip"
         ,"content": "second_content"
         ,"owner_id": test_user['id']}
        ,{"title": "NY trip"
         ,"content": "third_content"
         ,"owner_id": test_user['id']}
         ,{"title": "NY trip"
         ,"content": "third_content"
         ,"owner_id": test_user_2['id']}
    ]

    def create_post_model(posts):
        return models.Post(**posts)

    posts_map = list( map( create_post_model, posts_data))

    session.add_all(posts_map)
    session.commit()
    posts = session.query(models.Post).all()

    return posts
