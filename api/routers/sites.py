from schemas import SiteColor
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
async def get_sites(db: Session = Depends(get_db)):
    """Get a list of all sites."""
    return await SiteColor.get_all(db)

@router.put("/colors/{id}")
async def get_sites_sites(id: int, site_color: dict[str,str], db: Session = Depends(get_db)):
    """Update a site_color."""
    return await SiteColor.update(id, site_color, db)

