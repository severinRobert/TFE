from fastapi import status
from schemas import Field

field = Field(id=1, name="Prix", description="Le prix du produit", is_required=True, is_filterable=True, type_id=2, selections_group_id=None)
field2 = Field(id=2, name="Poids", description="Le poids du produit", is_required=False, is_filterable=False, type_id=4, selections_group_id=None)

class TestRouteFields:
    def test_add_field(self, client):
        # Add a fields
        response = client.post("/fields", json=field.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == field.dict()

        response = client.post("/fields", json=field2.dict())
        assert response.status_code == status.HTTP_200_OK
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