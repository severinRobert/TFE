from schemas import Type
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/types",
    tags=["types"],
)


@router.get("", response_model=list[Type])
async def get_types(db: Session = Depends(get_db)):
    """Get a list of all types."""
    return await Type.get_all(db)


@router.get("/{id}", response_model=Type)
async def get_type_id(id: int, db: Session = Depends(get_db)):
    """Get a type by id."""
    type = await Type.get(id, db)
    if not type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type with that id was found.")

    return type
