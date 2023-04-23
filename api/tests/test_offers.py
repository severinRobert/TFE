from fastapi import status
from schemas import Offer


offer = Offer(owner_id=1, product_id=1, states_id=1)
offer2 = Offer(owner_id=2, product_id=2, states_id=1)

class TestRouteOffers:

    def test_add_offer(self, client):
        # Add a offers
        response = client.post("/offers", json=offer.dict())
        assert response.status_code == status.HTTP_200_OK
        offer.id, offer.start_datetime = response.json()['id'], response.json()['start_datetime']
        assert response.json() == offer.dict()

        response = client.post("/offers", json=offer2.dict())
        assert response.status_code == status.HTTP_200_OK
        offer2.id, offer2.start_datetime = response.json()['id'], response.json()['start_datetime']
        assert response.json() == offer2.dict()

    def test_get_offer(self, client):
        # Also check that the path to the individual resource works
        response = client.get(f"/offers/{offer.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == offer.dict()

        response = client.get(f"/offers/{offer2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == offer2.dict()

        # Get a nonexistant resource should return 404
        response = client.get("/offers/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_offers(self, client):
        # Get all offers
        response = client.get("/offers")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        for offer in response.json():
            assert isinstance(offer, dict)
            assert {'id', 'owner_id', 'product_id', 'states_id', 'start_datetime', 'end_datetime'} == set(offer.keys())

    def test_update_offer(self, client):
        # Update a offer
        offer2.states_id = 2
        response = client.put(f"/offers/{offer2.id}", json=offer2.dict())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == offer2.dict()

        # Get the offer to check that it was updated
        response = client.get(f"/offers/{offer2.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == offer2.dict()

    def test_delete_offer(self, client):
        # Delete a offer
        response = client.delete(f"/offers/{offer.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Get the offer to check that it was deleted
        response = client.get(f"/offers/{offer.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete a nonexistant resource should return 404
        response = client.delete("/offers/666")
        assert response.status_code == status.HTTP_404_NOT_FOUND
