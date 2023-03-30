from typing import Optional

from models import Types
from pydantic import BaseModel, constr
from sqlalchemy import select
from sqlalchemy.orm import Session


class Type(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]

    class Config:
        orm_mode = True

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['type']:
        """Get a type from the database from its id."""
        type = db.query(Types).filter(Types.id == id).first()
        return type

    @classmethod
    async def get_all(cls, db: Session) -> list['type']:
        """Return a list of all Types from the database."""
        return db.query(Types).all()
