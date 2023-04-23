from fastapi import status
from schemas import Field
from tests.utils import with_user

field = Field(name="RAM", description="", is_required=True, is_filterable=True, type_id=1, selections_group_id=None)
field2 = Field(name="Screen Type", description="", is_required=False, is_filterable=True, type_id=2, selections_group_id=None)

class TestRouteFields:

    #@with_user("admin")
    def test_add_field(self, client):
        # Add a fields
        response = client.post("/fields", json=field.dict())
        assert response.status_code == status.HTTP_200_OK
        field.id = response.json()['id']
        assert response.json() == field.dict()
        

        response = client.post("/fields", json=field2.dict())
        assert response.status_code == status.HTTP_200_OK
        field2.id = response.json()['id']
        assert response.json() == field2.dict()

    def test_get_field(self, client):
        # Also check that the path to the individual resource works
        response = client.get(f"/fields/{field.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field.dict()

        response = client.get(f"/fields/{field2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field2.dict()

        # Get a nonexistant resource should return 404
        response = client.get("/fields/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fields(self, client):
        # Get all fields
        response = client.get("/fields")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        for field in response.json():
            assert isinstance(field, dict)
            assert {'id', 'name', 'description', 'is_required', 'is_filterable', 'type_id', 'selections_group_id'} == set(field.keys())

    def test_update_field(self, client):
        # Update a field
        print(field2.dict())
        field2.name = "Poids (kg)"
        print(field2.dict())
        response = client.put(f"/fields/{field2.id}", json=field2.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field2.dict()

        # Get the field to check that it was updated
        response = client.get(f"/fields/{field2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field2.dict()

    def test_delete_field(self, client):
        # Delete a field
        response = client.delete(f"/fields/{field.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Get the field to check that it was deleted
        response = client.get(f"/fields/{field.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete a nonexistant resource should return 404
        response = client.delete("/fields/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND
