from schemas import SiteColor, SiteSetting
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from utils import model_to_dict


router = APIRouter(
    prefix="/sites",
    tags=["sites"],
)

@router.get("/colors", response_model=list[SiteColor])
async def get_sites_colors(db: Session = Depends(get_db)):
    """Get a list of all sites."""
    return await SiteColor.get_all(db)

@router.put("/colors/{id}", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def put_site_color(id: int, site_color: dict[str,str], db: Session = Depends(get_db)):
    """Update a site_color."""
    return await SiteColor.update(id, site_color, db)

@router.get("/settings", response_model=SiteSetting)
async def get_sites_settings(db: Session = Depends(get_db)):
    """Get a list of all sites."""
    return await SiteSetting.get(1, db)

@router.put("/settings", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def put_site_setting(site_setting: dict[str,str], db: Session = Depends(get_db)):
    """Update a site_setting."""
    return await SiteSetting.update(1, site_setting, db)
