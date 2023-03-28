from fastapi.testclient import TestClient
from main import app
from . import tests

client = TestClient(app)

