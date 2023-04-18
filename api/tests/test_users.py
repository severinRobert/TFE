from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import User

bob = User(id=1, username="bob", email="bob@gmail.com", password="bob", state_id=1)
alice = User(id=2, username="alice", email="alice@gmail.com", password="alice", state_id=1)
hacker1 = User(id=3, username="hacker", email="bob@gmail.com", password="hacker", state_id=1)
hacker2 = User(id=4, username="alice", email="hacker@gmail.com", password="hacker", state_id=1)

auth_bob_mail = {"username": "bob@gmail.com", "password": "bob", "grant_type": "password"}
auth_bob_username = {"username": "bob", "password": "bob", "grant_type": "password"}
auth_alice_mail = {"username": "alice@gmail.com", "password": "alice", "grant_type": "password"}
auth_alice_username = {"username": "alice", "password": "alice", "grant_type": "password"}
auth_hacker1_mail = {"username": "alice@gmail.com", "password": "hacker", "grant_type": "password"}
auth_hacker1_username = {"username": "alice", "password": "hacker", "grant_type": "password"}

def is_response_token(response):
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()['access_token'], str)
    assert response.json()['token_type'] == "bearer"

class TestRouteUsers:

    def test_register(self, client):
        # Add Bob and Alice
        response = client.post("/users/register", json=bob.dict())
        is_response_token(response)

        response = client.post("/users/register", json=alice.dict())
        is_response_token(response)

        # Add a user with an existing username or email
        assert client.post("/users/register", json=hacker1.dict()).status_code == status.HTTP_400_BAD_REQUEST
        assert client.post("/users/register", json=hacker2.dict()).status_code == status.HTTP_400_BAD_REQUEST

    def test_login(self, client):
        # Login users
        response = client.post("/users/login", data=auth_bob_mail)
        is_response_token(response)
        response = client.post("/users/login", data=auth_bob_username)
        is_response_token(response)

        response = client.post("/users/login", data=auth_alice_mail)
        is_response_token(response)
        response = client.post("/users/login", data=auth_alice_username)
        is_response_token(response)

        # Login with wrong credentials
        assert client.post("/users/login", data=auth_hacker1_mail).status_code == status.HTTP_401_UNAUTHORIZED
        assert client.post("/users/login", data=auth_hacker1_username).status_code == status.HTTP_401_UNAUTHORIZED

