import pytest
from fastapi import status
from fastapi.testclient import TestClient
from schemas import Field

class TestRouteFields:
    async def test_add_field(self, client: TestClient, field2: Field):
        # Add a field
        response = await client.post("/fields", json=field2.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field2.dict()

        # Check if the field we added has been added.
        # We run the tests against a fresh database every time, so it should contain only our field.
        response = await client.get(f"/fields/{field2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field2.dict()

    async def test_get_field(self, client: TestClient, field: Field):
        # Also check that the path to the individual resource works
        response = await client.get(f"/fields/{field.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field.dict()

        # Get a nonexistant resource should return 404
        response = await client.get("/fields/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND