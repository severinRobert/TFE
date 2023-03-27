from schemas import Product, ProductField
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

@router.get("/{id}/fields", response_model=list[Product])

@router.put("/{id}", response_model=Product)
async def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    """Update a product."""
    product = product.dict()
    product.pop('id')
    return await Product.update(id, db, **product)

@router.patch("/{id}", response_model=Product)
async def edit_product(id: int, product: Product, db: Session = Depends(get_db)):
    """Edit a product."""
    product = product.dict()
    product.pop('id')
    return await Product.edit(id, db, product)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: Session = Depends(get_db)):
    """Delete a product."""
    product = await Product.get(id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")

    await Product.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
