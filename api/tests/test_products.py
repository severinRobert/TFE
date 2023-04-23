from fastapi import status
from schemas import Product, ProductField, Offer

smartphone = Product(name="Smartphone", description="A phone that is smart")
laptop = Product(name="Laptop", description="A portable PC")

class TestRouteProducts:
    def test_add_product(self, client):
        # Add a products
        response = client.post("/products", json=smartphone.dict())
        assert response.status_code == status.HTTP_200_OK
        smartphone.id = response.json()['id']
        assert response.json() == smartphone.dict()

        response = client.post("/products", json=laptop.dict())
        assert response.status_code == status.HTTP_200_OK
        laptop.id = response.json()['id']
        assert response.json() == laptop.dict()

        # Add a product that already exists
        response = client.post("/products", json=laptop.dict())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Product already exists'}

    def test_get_product(self, client):
        # Also check that the path to the individual resource works
        response = client.get(f"/products/{smartphone.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == smartphone.dict()

        response = client.get(f"/products/{laptop.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == laptop.dict()

        # Get a nonexistant resource should return 404
        response = client.get("/products/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_products(self, client):
        # Get all products
        response = client.get("/products")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        for product in response.json():
            assert isinstance(product, dict)
            assert 'id' in product
            assert 'name' in product
            assert 'description' in product

    def test_update_product(self, client):
        # Update a product
        laptop.name = "Portable PC"
        response = client.put(f"/products/{laptop.id}", json=laptop.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == laptop.dict()

        # Get the product to check that it was updated
        response = client.get(f"/products/{laptop.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == laptop.dict()

    def test_delete_product(self, client):
        # Delete a product
        response = client.delete(f"/products/{smartphone.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.get(f"/products/{smartphone.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete a nonexistant resource should return 404
        response = client.delete("/products/666")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Product does not exist'}

        # Delete a product that is linked to offers
        # Add product_field to laptop
        product_field = ProductField(product_id=laptop.id, field_id=1)
        response = client.post(f"/product_fields", json=product_field.dict())
        assert response.status_code == status.HTTP_200_OK
        product_field.id = response.json()['id']
        response = client.get(f"/product_fields/{product_field.id}")
        assert response.status_code == status.HTTP_200_OK
        # Add offer to laptop
        offer = Offer(owner_id=1, product_id=laptop.id, states_id=1)
        response = client.post(f"/offers", json=offer.dict())
        assert response.status_code == status.HTTP_200_OK
        offer.id = response.json()['id']
        # Try to delete laptop
        response = client.delete(f"/products/{laptop.id}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Product is linked to offers'}
        # Delete offer
        response = client.delete(f"/offers/{offer.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Delete product
        response = client.delete(f"/products/{laptop.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Check that product_field was deleted
        response = client.get(f"/product_fields/{product_field.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
