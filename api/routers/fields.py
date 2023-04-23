from schemas import Field
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer


router = APIRouter(
    prefix="/fields",
    tags=["fields"],
)

@router.post("", response_model=Field) #, dependencies=[Depends(JWTBearer())]
async def add_field(field: Field, db: Session = Depends(get_db)):
    """Add a field."""
    return await Field.add(field, db)


@router.get("", response_model=list[Field])
async def get_fields(db: Session = Depends(get_db)):
    """Get a list of all fields."""
    return await Field.get_all(db)


@router.get("/{id}", response_model=Field)
async def get_field_id(id: int, db: Session = Depends(get_db)):
    """Get a field by id."""
    field = await Field.get(id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")

    return field

@router.put("/{id}", response_model=Field)
async def update_field(id: int, field: Field, db: Session = Depends(get_db)):
    """Update a field."""
    field = field.dict()
    field.pop('id')
    return await Field.update(id, db, **field)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(id: int, db: Session = Depends(get_db)):
    """Delete a field."""
    field = await Field.get(id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")

    await Field.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
