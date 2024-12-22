from app import schemas
import pytest
from jose import JWTError, jwt
from app.config import settings



# def test_root(client, session):
#     session.query()
#     res = client.get("/")
#     # print(res.json())
#     print(res.json())
#     assert res.json().get('message') == 'welcome to my API !'
    # assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "obama@gmail.com", "password": "password123"})
    new_user = schemas.Userout(**res.json())
    assert new_user.email == "obama@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    # print(res.json())
    login_res = schemas.Token(**res.json())
    
    # some more validation
    payload = jwt.decode(login_res.access_token, settings.secret_key, [settings.algorithm]) 
    id = payload.get("user_id")
    
    # print(login_res)
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'wrongpass', 403),
    ('yadnesh@gmail.com', 'wrongpass', 403),
    ('wrongemail@gmail.com', 'wrongpass', 403),
    (None, 'password123', 403),
    ('obama@gmail.com', None, 403)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    # print(res.json())
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'