from schemas import User
from fastapi.testclient import TestClient
from main import app


def with_user(user):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("$$$$", args)
            print("$$$$", args[1])
            print("$$$$", user)
            client = TestClient(app)
            response = client.post("/users/login", json=user.dict())
            
            return func(*args, **kwargs)
        return wrapper
    return decorator