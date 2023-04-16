from typing import Optional

from models import States
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session


class State(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]

    class Config:
        orm_mode = True

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['state']:
        """Get a state from the database from its id."""
        state = db.query(States).filter(States.id == id).first()
        return state

    @classmethod
    async def get_all(cls, db: Session) -> list['state']:
        """Return a list of all States from the database."""
        return db.query(States).all()
