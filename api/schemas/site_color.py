from typing import Optional

from models import SiteColors
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session


class SiteColor(BaseModel):
    id: Optional[int]
    name: constr(max_length=40)
    value: Optional[constr(max_length=40)]
    value_dark: Optional[constr(max_length=40)]

    class Config:
        orm_mode = True

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['site_color']:
        """Get a site_color from the database from its id."""
        site_color = db.query(SiteColors).filter(SiteColors.id == id).first()
        return site_color

    @classmethod
    async def get_all(cls, db: Session) -> list['site_color']:
        """Return a list of all SiteColors from the database."""
        return db.query(SiteColors).all()

    @classmethod
    async def update(cls, id: int, site_color: dict, db: Session) -> Optional['site_color']:
        """Update site_colors of a site_color."""
        db_site_color = await cls.get(id, db)
        if db_site_color:
            for key, value in site_color.items():
                setattr(db_site_color, key, value)
            db.commit()
            db.refresh(db_site_color)
        return db_site_color
