from typing import Optional
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from models import Offers
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class Offer(BaseModel):
    id: Optional[int]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    owner_id: int
    product_id: int
    states_id: int

    class Config:
        orm_mode = True

    @classmethod
    async def add(cls, offer: 'Offer', db: Session) -> 'Offer':
        """Add a offer to the database."""
        values = jsonable_encoder(offer)
        values.pop('id')
        values['start_datetime'] = datetime.now()
        db_offer = Offers(**values)
        
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return db_offer

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['offer']:
        """Get a offer from the database from its id."""
        offer = db.query(Offers).filter(Offers.id == id).first()
        return offer
    
    @classmethod
    async def get_by_product_id(cls, product_id: int, db: Session) -> Optional['offer']:
        """Get a offer from the database from its id."""
        offer = db.query(Offers).filter(Offers.product_id == product_id).first()
        return offer

    @classmethod
    async def get_all(cls, db: Session) -> list['offer']:
        """Return a list of all Offers from the database."""
        return db.query(Offers).all()

    @classmethod
    async def update(cls, id: int, db: Session, **kwargs) -> Optional['offer']:
        """Update offers of a offer."""
        offer = await cls.get(id, db)
        if offer:
            for key, value in kwargs.items():
                setattr(offer, key, value)
            db.commit()
        return offer

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['offer']:
        """Delete a offer and return it. Return None if the offer does not exists."""
        offer = await cls.get(id, db)
        if offer:
            db.delete(offer)
            db.commit()
        return offer
