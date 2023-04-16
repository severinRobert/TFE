from fastapi import status
from schemas import State


class TestRouteStates:

    def test_get_state(self, client):
        # Get a state
        response = client.get("/states/1")
        assert response.status_code == status.HTTP_200_OK
        # Check that the state is in the response
        assert isinstance(response.json(), dict)
        assert State(**response.json())

        response = client.get("/states/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_states(self, client):
        # Get all states
        response = client.get("/states")
        assert response.status_code == status.HTTP_200_OK
        # Check that the states are in the response
        assert isinstance(response.json(), list)
        for s in response.json():
            assert isinstance(s, dict)
            assert State(**s)
