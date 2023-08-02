from schemas import Field, ProductField
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer


router = APIRouter(
    prefix="/fields",
    tags=["fields"],
)

@router.post("", response_model=Field, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_field(field: Field, db: Session = Depends(get_db)):
    """Add a field."""
    return await Field.add(field, db)

async def t(details, db, schema):
    """
    {
        3:{
            "name": "gre",
            "type": "update"
        },
        6:{
            "type": "delete"
        },
        "new1":{
            "name": "purple",
            "description": "Purple",
            "id": "new1",
            "type": "add"
        }
    }
    """
    to_verify = []
    print(details)
    for id, detail in details['changes'].items():
        if detail['type'] == 'update':
            if not details['force']:
                #TODO add a check to see if the selection is used in an offer
                # if Fields with selections_groups_id and have a value with selections_id
                pass
            detail.pop('type')
            await schema.update(id, detail, db)
        elif detail['type'] == 'delete':
            if not details['force']:
                #TODO add a check to see if the selection is used in an offer
                # if Fields with selections_groups_id and have a value with selections_id
                #ValueInt.get_by_value(id, db)
                pass
            product_field_db = await ProductField.get_by_product_id_and_field_id(details['product_id'], id, db)
            if product_field_db:
                await ProductField.delete(product_field_db.id, db)
        elif detail['type'] == 'add':
            if type(detail['id']) == str:
                print("add field")
                field_db = await schema.add(Field(name=detail['name'], display_name=detail['display_name'],
                                                  description=detail['description'], is_required=detail['is_required'],
                                                  is_filterable=detail['is_filterable'], type_id=detail['type_id'],
                                                  selections_groups_id=detail['selections_groups_id']), db)
            else:
                print("get field")
                field_db = await schema.get(detail['id'], db)
            print("add product field")
            await ProductField.add(ProductField(product_id=details['product_id'], field_id=field_db.id), db)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid type.")
    if to_verify:
        # raise error and send to_verfy to frontend
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="The selection is used in an offer.", 
                            headers={"to_verify": to_verify})

@router.post("/details", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_selection(details: dict[str, int | dict], db: Session = Depends(get_db)):
    return await t(details, db, Field)

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

@router.put("/{id}", response_model=Field, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def update_field(id: int, field: Field, db: Session = Depends(get_db)):
    """Update a field."""
    field = field.dict()
    field.pop('id')
    return await Field.update(id, db, **field)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def delete_field(id: int, db: Session = Depends(get_db)):
    """Delete a field."""
    field = await Field.get(id, db)
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No field with that id was found.")

    await Field.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
