from schemas import Field, Image, ProductField, Selection, User, ValueBool, ValueFloat, ValueInt, ValueString
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from utils import model_to_dict, INT_TYPES, STRING_TYPES, FLOAT_TYPES, BOOL_TYPES


router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("", dependencies=[Depends(JWTBearer(role="User"))]) #response_model=Image, 
async def add_image(image: Image, db: Session = Depends(get_db)):
    """Add an image."""
    return await Image.add(image, db)

@router.get("", response_model=list[Image])
async def get_images(db: Session = Depends(get_db)):
    """Get a list of all images."""
    return await Image.get_all(db)

@router.get("/{id}", response_model=Image)
async def get_image_id(id: int, db: Session = Depends(get_db)):
    """Get a image by id."""
    image = await Image.get(id, db)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image with that id was found.")

    return image

@router.put("/{id}", response_model=Image, dependencies=[Depends(JWTBearer(role="User"))])
async def update_image(id: int, image: Image, db: Session = Depends(get_db)):
    """Update a image."""
    image = image.dict()
    image.pop('id')
    return await Image.update(id, db, **image)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(role="User"))])
async def delete_image(id: int, db: Session = Depends(get_db)):
    """Delete a image."""
    image = await Image.get(id, db)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image with that id was found.")

    await Image.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
