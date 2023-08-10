from typing import Optional

from models import SiteSettings
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session


class SiteSetting(BaseModel):
    id: Optional[int]
    title: constr(max_length=40)
    home_description: constr(max_length=500)

    class Config:
        orm_mode = True

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['site_setting']:
        """Get a site_setting from the database from its id."""
        site_setting = db.query(SiteSettings).filter(SiteSettings.id == id).first()
        return site_setting

    @classmethod
    async def update(cls, id: int, site_setting: dict, db: Session) -> Optional['site_setting']:
        """Update site_settings of a site_setting."""
        db_site_setting = await cls.get(id, db)
        if db_site_setting:
            for key, value in site_setting.items():
                setattr(db_site_setting, key, value)
            db.commit()
            db.refresh(db_site_setting)
        return db_site_setting
