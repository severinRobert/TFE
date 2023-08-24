from typing import Optional

from models import Products
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
from .product_field import ProductField
from .offer import Offer


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

        if db.query(Products).filter(Products.name == product.name).first():
            raise Exception("Product already exists")

        values = product.dict()
        values.pop('id')
        db_product = Products(**values)
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

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
    async def delete(cls, id: int, db: Session, force: bool = False) -> Optional['product']:
        """Delete a product and return it. Return None if the product does not exists."""
        product = await cls.get(id, db)
        if not product:
            raise Exception("Product does not exist")

        offers = await Offer.get_by_product_id(id, db)
        if offers and not force:
            raise Exception("Product is linked to offers")
        for offer in offers:
            await Offer.delete(offer.id, db)

        product_fields = await ProductField.get_by_product_id(id, db)
        for product_field in product_fields:
            await ProductField.delete(product_field.id, db)

        db.delete(product)
        db.commit()
        return product
