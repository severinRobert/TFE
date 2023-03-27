from typing import Optional

from models import Fields
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class Field(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]
    is_required: bool
    is_filterable: bool
    type_id: int
    selections_group_id: Optional[int]

    class Config:
        orm_mode = True

    @classmethod
    async def add(cls, field: 'Field', db: Session) -> 'Field':
        """
        Add a field to the database.
        The field's id is auto generated by the database.
        The id is suppressed without warning.
        """
        values = field.dict()
        values.pop('id')
        
        db.add(Fields(**values))
        db.commit()
        
        return field

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['field']:
        """Get a field from the database from its id."""
        field = db.query(Fields).filter(Fields.id == id).first()
        return field

    @classmethod
    async def get_all(cls, db: Session) -> list['field']:
        """Return a list of all Fields from the database."""
        return db.query(Fields).all()

    @classmethod
    async def update(cls, id: int, db: Session, **kwargs) -> Optional['field']:
        """Update fields of a field."""
        field = await cls.get(id, db)
        if field:
            for key, value in kwargs.items():
                setattr(field, key, value)
            db.commit()
        return field

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['field']:
        """Delete a field and return it. Return None if the field does not exists."""
        field = await cls.get(id, db)
        if field:
            print("Deleting field")
            db.delete(field)
            db.commit()
        return field
