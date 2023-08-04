from typing import Optional
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from models import Images
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class Image(BaseModel):
    id: Optional[int]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    owner_id: int
    product_id: int
    states_id: int

    class Config:
        orm_mode = True

    @classmethod
    async def add(cls, image: 'Image', db: Session) -> 'Image':
        """Add a image to the database."""
        values = jsonable_encoder(image)
        values.pop('id')
        values['start_datetime'] = datetime.now()
        db_image = Images(**values)
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['image']:
        """Get a image from the database from its id."""
        image = db.query(Images).filter(Images.id == id).first()
        return image
    
    @classmethod
    async def get_by_product_id(cls, product_id: int, db: Session) -> Optional['image']:
        """Get a image from the database from its id."""
        images = db.query(Images).filter(Images.product_id == product_id).all()
        print(images)
        return images
    
    @classmethod
    async def get_by_user_id(cls, owner_id: int, db: Session) -> Optional['image']:
        """Get a image from the database from its id."""
        images = db.query(Images).filter(Images.owner_id == owner_id).all()
        print(images)
        return images

    @classmethod
    async def get_all(cls, db: Session) -> list['image']:
        """Return a list of all Images from the database."""
        return db.query(Images).all()

    @classmethod
    async def update(cls, id: int, db: Session, **kwargs) -> Optional['image']:
        """Update images of a image."""
        image = await cls.get(id, db)
        if image:
            for key, value in kwargs.items():
                setattr(image, key, value)
            db.commit()
        return image

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['image']:
        """Delete a image and return it. Return None if the image does not exists."""
        image = await cls.get(id, db)
        if image:
            values = [*await ValueString.get_by_image_id(image.id, db), *await ValueInt.get_by_image_id(image.id, db), *await ValueFloat.get_by_image_id(image.id, db), *await ValueBool.get_by_image_id(image.id, db)]
            for value in values:
                db.delete(value)
            db.commit()
            db.delete(image)
            db.commit()
        return image
