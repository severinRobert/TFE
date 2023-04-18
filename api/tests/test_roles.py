from fastapi import status
from schemas import Role


class TestRouteRoles:

    def test_get_role(self, client):
        # Get a role
        response = client.get("/roles/1")
        assert response.status_code == status.HTTP_200_OK
        # Check that the role is in the response
        assert isinstance(response.json(), dict)
        assert Role(**response.json())

        response = client.get("/roles/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_roles(self, client):
        # Get all roles
        response = client.get("/roles")
        assert response.status_code == status.HTTP_200_OK
        # Check that the roles are in the response
        assert isinstance(response.json(), list)
        for t in response.json():
            assert isinstance(t, dict)
            assert Role(**t)
