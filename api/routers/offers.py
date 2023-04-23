from schemas import Offer
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)

@router.post("", response_model=Offer)
async def add_offer(offer: Offer, db: Session = Depends(get_db)):
    """Add a offer."""
    print("add",offer)
    return await Offer.add(offer, db)


@router.get("", response_model=list[Offer])
async def get_offers(db: Session = Depends(get_db)):
    """Get a list of all offers."""
    return await Offer.get_all(db)


@router.get("/{id}", response_model=Offer)
async def get_offer_id(id: int, db: Session = Depends(get_db)):
    """Get a offer by id."""
    offer = await Offer.get(id, db)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offer with that id was found.")

    return offer

@router.put("/{id}", response_model=Offer)
async def update_offer(id: int, offer: Offer, db: Session = Depends(get_db)):
    """Update a offer."""
    offer = offer.dict()
    offer.pop('id')
    return await Offer.update(id, db, **offer)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(id: int, db: Session = Depends(get_db)):
    """Delete a offer."""
    offer = await Offer.get(id, db)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offer with that id was found.")

    await Offer.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
