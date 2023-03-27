from typing import Optional

from models import Products
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class Product(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]

    class Config:
        orm_mode = True

    @classmethod
    async def add(cls, product: 'Product', db: Session) -> 'Product':
        """
        Add a product to the database.
        The product's id is auto generated by the database.
        The id is suppressed without warning.
        """
        values = product.dict()
        values.pop('id')
        
        db.add(Products(**values))
        db.commit()
        db.refresh(product)
        
        return product

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['product']:
        """Get a product from the database from its id."""
        product = db.query(Products).filter(Products.id == id).first()
        return product

    @classmethod
    async def get_all(cls, db: Session) -> list['product']:
        """Return a list of all Products from the database."""
        return db.query(Products).all()

    @classmethod
    async def update(cls, id: int, db: Session, **kwargs) -> Optional['product']:
        """Update products of a product."""
        product = await cls.get(id, db)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            db.commit()
        return product

    @classmethod
    async def edit(cls, id: int, db: Session, product: 'product') -> Optional['product']:
        """Edit a product using another product object."""
        return await cls.update(id, db, **product)

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['product']:
        """Delete a product and return it. Return None if the product does not exists."""
        product = await cls.get(id, db)
        if product:
            print("Deleting product")
            db.delete(product)
            db.commit()
        return product
