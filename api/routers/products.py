from schemas import Product, ProductField, Field
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("", response_model=Product)
async def add_product(product: Product, db: Session = Depends(get_db)):
    """Add a product."""
    return await Product.add(product, db)


@router.get("", response_model=list[Product])
async def get_products(db: Session = Depends(get_db)):
    """Get a list of all products."""
    return await Product.get_all(db)


@router.get("/{id}", response_model=Product)
async def get_product_id(id: int, db: Session = Depends(get_db)):
    """Get a product by id."""
    product = await Product.get(id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")

    return product

@router.get("/{id}/fields", response_model=list[Field])
async def get_product_fields(id: int, db: Session = Depends(get_db)):
    """Get a product's fields by id."""
    product = await Product.get(id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")
    product_fields = await ProductField.get_by_product_id(id, db)
    if not product_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product_field with that product_id was found.")
    print("++++++", product_fields)
    return [await Field.get(product_field.field_id, db) for product_field in product_fields]

@router.post("/{product_id}/fields/{field_id}", response_model=ProductField)
async def add_product_field(product_id: int, field_id: int, db: Session = Depends(get_db)):
    """Add a product_field."""
    product = await Product.get(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")
    field = await Field.get(field_id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")
    product_field = ProductField(product_id=product_id, field_id=field_id)
    return await ProductField.add(product_field, db)

@router.put("/{id}", response_model=Product)
async def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    """Update a product."""
    product = product.dict()
    product.pop('id')
    return await Product.update(id, db, **product)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: Session = Depends(get_db)):
    """Delete a product."""
    product = await Product.get(id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")

    await Product.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
