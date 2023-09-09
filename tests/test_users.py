
from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))

    assert res.json().get('message') == 'Hello World!'
    assert res.status_code == 200



def test_create_user(client):
    res = client.post("/users/", json={"email": "teess@tess.com", "password": "whatever"})
    
    print(res.json())

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201



def test_login_user(client,test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}) #data to imitate a form request
    print(res.json())
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)

    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    (None, 'pass', 422),
    ('test_user@user.com', "falsepass", 403),
    ('uiuiui@user.com', "falsepass", 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
