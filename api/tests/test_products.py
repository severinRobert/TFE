from fastapi import status
from schemas import Product

product = Product(id=1, name="Prix", description="Le prix du produit", is_required=True, is_filterable=True, type_id=2, selections_group_id=None)
product2 = Product(id=2, name="Poids", description="Le poids du produit", is_required=False, is_filterable=False, type_id=4, selections_group_id=None)

class TestRouteProducts:
    def test_add_product(self, client):
        # Add a products
        response = client.post("/products", json=product.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product.dict()

        response = client.post("/products", json=product2.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product2.dict()

    def test_get_product(self, client):
        # Also check that the path to the individual resource works
        response = client.get(f"/products/{product.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product.dict()

        response = client.get(f"/products/{product2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product2.dict()

        # Get a nonexistant resource should return 404
        response = client.get("/products/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_products(self, client):
        # Get all products
        response = client.get("/products")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [product.dict(), product2.dict()]

    def test_update_product(self, client):
        # Update a product
        print(product2.dict())
        product2.name = "Poids (kg)"
        print(product2.dict())
        response = client.put(f"/products/{product2.id}", json=product2.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product2.dict()

        # Get the product to check that it was updated
        response = client.get(f"/products/{product2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product2.dict()

    def test_delete_product(self, client):
        # Delete a product
        response = client.delete(f"/products/{product.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Get the product to check that it was deleted
        response = client.get(f"/products/{product.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete a nonexistant resource should return 404
        response = client.delete("/products/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND
