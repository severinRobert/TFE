from fastapi import status
from schemas import User

bob = User(id=1, username="bob", email="bob@gmail.com", password="bob", state_id=1)
alice = User(id=2, username="alice", email="alice@gmail.com", password="alice", state_id=1)
hacker1 = User(id=3, username="hacker", email="bob@gmail.com", password="hacker", state_id=1)
hacker2 = User(id=4, username="alice", email="hacker@gmail.com", password="hacker", state_id=1)

class TestRouteUsers:

    def test_register(self, client):
        # Add Bob and Alice
        assert client.post("/users/register", json=bob.dict()).status_code == status.HTTP_201_CREATED
        assert client.post("/users/register", json=alice.dict()).status_code == status.HTTP_201_CREATED

        # Add a user with an existing username or email
        assert client.post("/users/register", json=hacker1.dict()).status_code == status.HTTP_400_BAD_REQUEST
        assert client.post("/users/register", json=hacker2.dict()).status_code == status.HTTP_400_BAD_REQUEST

    def test_login(self, client):
        # Login users
        assert client.post("/users/login", json=bob.dict()).status_code == status.HTTP_200_OK
        assert client.post("/users/login", json=alice.dict()).status_code == status.HTTP_200_OK

        # Login with wrong credentials
        assert client.post("/users/login", json=hacker1.dict()).status_code == status.HTTP_400_BAD_REQUEST
        assert client.post("/users/login", json=hacker2.dict()).status_code == status.HTTP_400_BAD_REQUEST
