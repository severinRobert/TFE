from fastapi import status
from schemas import ProductField

product_field = ProductField(product_id=5, field_id=6)
product_field2 = ProductField(product_id=4, field_id=6)

class TestRouteProductFields:

    def test_add_product_field(self, client):
        # Add a product_fields
        response = client.post("/product_fields", json=product_field.dict())
        assert response.status_code == status.HTTP_200_OK
        product_field.id = response.json()['id']
        assert response.json() == product_field.dict()

        response = client.post("/product_fields", json=product_field2.dict())
        assert response.status_code == status.HTTP_200_OK
        product_field2.id = response.json()['id']
        assert response.json() == product_field2.dict()

    def test_get_product_field(self, client):
        # Also check that the path to the individual resource works
        response = client.get(f"/product_fields/{product_field.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product_field.dict()

        response = client.get(f"/product_fields/{product_field2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product_field2.dict()

        # Get a nonexistant resource should return 404
        response = client.get("/product_fields/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_product_fields(self, client):
        # Get all product_fields
        response = client.get("/product_fields")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        for product in response.json():
            assert isinstance(product, dict)
            assert 'id' in product
            assert 'product_id' in product
            assert 'field_id' in product

    def test_delete_product_field(self, client):
        # Delete a product_field
        response = client.delete(f"/product_fields/{product_field.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Get the product_field to check that it was deleted
        response = client.get(f"/product_fields/{product_field.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete a nonexistant resource should return 404
        response = client.delete("/product_fields/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND
