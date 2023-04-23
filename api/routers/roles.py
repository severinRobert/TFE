from schemas import Role
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.get("", response_model=list[Role])
async def get_roles(db: Session = Depends(get_db)):
    """Get a list of all roles."""
    return await Role.get_all(db)


@router.get("/{id}", response_model=Role)
async def get_role_id(id: int, db: Session = Depends(get_db)):
    """Get a role by id."""
    role = await Role.get(id, db)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No role with that id was found.")

    return role