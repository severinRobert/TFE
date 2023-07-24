from typing import Optional

from models import SelectionsGroups, Selections
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class SelectionsGroup(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]

    class Config:
        orm_mode = True

    @classmethod
    async def add(cls, selections_group: 'SelectionsGroup', db: Session) -> 'SelectionsGroup':
        """
        Add a selections_group to the database.
        The selections_group's id is auto generated by the database.
        The id is suppressed without warning.
        """
        values = selections_group.dict()
        values.pop('id')
        db_selections_group = SelectionsGroups(**values)
        
        db.add(db_selections_group)
        db.commit()
        db.refresh(db_selections_group)
        return db_selections_group

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['selections_group']:
        """Get a selections_group from the database from its id."""
        selections_group = db.query(SelectionsGroups).filter(SelectionsGroups.id == id).first()
        return selections_group
    
    @classmethod
    async def get_by_name(cls, name: str, db: Session) -> Optional['selections_group']:
        """Get a selections_group from the database from its name."""
        selections_group = db.query(SelectionsGroups).filter(SelectionsGroups.name == name).first()
        return selections_group

    @classmethod
    async def get_all(cls, db: Session) -> list['selections_group']:
        """Return a list of all SelectionsGroups from the database."""
        return db.query(SelectionsGroups).all()

    @classmethod
    async def update(cls, id: int, selections_group: dict, db: Session) -> Optional['selections_group']:
        """Update a selections_group and return it. Return None if the selections_group does not exists."""
        db_selections_group = await cls.get(id, db)
        if db_selections_group:
            for key, value in selections_group.items():
                setattr(db_selections_group, key, value)
            db.commit()
            db.refresh(db_selections_group)
        return db_selections_group

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['selections_group']:
        """Delete a selections_group and return it. Return None if the selections_group does not exists."""
        selections_group = await cls.get(id, db)
        if selections_group:
            db.query(Selections).filter(Selections.selections_groups_id == id).delete()
            db.delete(selections_group)
            db.commit()
        return selections_group
