from schemas import Product, ProductField, Field
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/product_fields",
    tags=["product_fields"],
)

@router.post("", response_model=ProductField)
async def add_product_field(product_field: ProductField, db: Session = Depends(get_db)):
    """Add a product_field."""
    if not await Product.get(product_field.product_id, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No product with that id was found.")
    if not await Field.get(product_field.field_id, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field with that id was found.")
    if await ProductField.get_by_product_id_and_field_id(product_field.product_id, product_field.field_id, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A product_field with that product_id and field_id already exists.")
    return await ProductField.add(product_field, db)

@router.get("", response_model=list[ProductField])
async def get_product_fields(db: Session = Depends(get_db)):
    """Get a list of all product_fields."""
    return await ProductField.get_all(db)

@router.get("/{id}", response_model=ProductField)
async def get_product_field_id(id: int, db: Session = Depends(get_db)):
    """Get a product_field by id."""
    product_field = await ProductField.get(id, db)
    if not product_field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that id was found.")

    return product_field

@router.get("/product/{id}", response_model=list[Field])
async def get_product_field_id_by_product(id: int, db: Session = Depends(get_db)):
    """Get all fields for a product by id."""
    product = await Product.get(id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")
    product_fields = await ProductField.get_by_product_id(id, db)
    if not product_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that product_id was found.")
    return [await Field.get(product_field.field_id, db) for product_field in product_fields]

@router.get("/field/{id}", response_model=list[Product])
async def get_product_field_id_by_field(id: int, db: Session = Depends(get_db)):
    """Get all products for a field by id."""
    field = await Field.get(id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")
    product_fields = await ProductField.get_by_field_id(id, db)
    if not product_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that field_id was found.")
    return [await Product.get(product_field.product_id, db) for product_field in product_fields]

@router.get("/product/{product_id}/field/{field_id}", response_model=ProductField)
async def get_product_field_id_by_product_and_field(product_id: int, field_id: int, db: Session = Depends(get_db)):
    """Get a product_field by product_id and field_id."""
    product = await Product.get(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")
    field = await Field.get(field_id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")
    product_field = await ProductField.get_by_product_id_and_field_id(product_id, field_id, db)
    if not product_field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that product_id and field_id was found.")
    return product_field

@router.put("/{id}", response_model=ProductField)
async def update_product_field(id: int, product_field: ProductField, db: Session = Depends(get_db)):
    """Update a product_field."""
    product_field = product_field.dict()
    product_field.pop('id')
    return await ProductField.update(id, db, **product_field)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_field(id: int, db: Session = Depends(get_db)):
    """Delete a product_field."""
    product_field = await ProductField.get(id, db)
    if not product_field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that id was found.")

    await ProductField.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
