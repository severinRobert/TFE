from fastapi import status
from schemas import Type


class TestRouteTypes:

    def test_get_type(self, client):
        # Get a type
        response = client.get("/types/1")
        assert response.status_code == status.HTTP_200_OK
        # Check that the type is in the response
        assert isinstance(response.json(), dict)
        assert Type(**response.json())

        response = client.get("/types/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_types(self, client):
        # Get all types
        response = client.get("/types")
        assert response.status_code == status.HTTP_200_OK
        # Check that the types are in the response
        assert isinstance(response.json(), list)
        for t in response.json():
            assert isinstance(t, dict)
            assert Type(**t)
