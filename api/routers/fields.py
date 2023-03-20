from schemas.fields import Field
from fastapi import HTTPException, status, APIRouter, Response



router = APIRouter(
    prefix="/fields",
    tags=["fields"],
)

@router.post("", response_model=Field)
async def add_field(field: Field):
    """Add a field."""
    return await Field.add(field)


@router.get("")#, response_model=list[Field])
async def get_fields():
    """Get a list of all fields."""
    return {"status": "success", "note": "test"}#await Field.get_all()


@router.get("/{id}", response_model=Field)
async def get_field_id(id: int):
    """Get a field by id."""
    field = await Field.get(id)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")

    return field
