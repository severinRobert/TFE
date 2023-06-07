from schemas import Field, Offer, ProductField, Selection, User, ValueBool, ValueFloat, ValueInt, ValueString
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from utils import model_to_dict, INT_TYPES, STRING_TYPES, FLOAT_TYPES, BOOL_TYPES


router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)

@router.post("", dependencies=[Depends(JWTBearer(role="User"))]) #response_model=Offer, 
async def add_offer(offer: Offer, db: Session = Depends(get_db)):
    """Add an offer."""
    return await Offer.add(offer, db)

@router.post("/details", dependencies=[Depends(JWTBearer(role="User"))]) #response_model=Offer, 
async def add_offer(values: dict, db: Session = Depends(get_db)):
    """Add an offer with fields details.
        {
            "owner_id": 0,
            "product_id": 0,
            "fields": {
                "1": value,
                ...
            }
        }
    """
    print("add",values)
    # create offer
    offer = values.copy()
    offer.pop('fields')
    print(offer)
    offer['states_id'] = 2
    offer = await Offer.add(Offer(**offer), db)
    print(offer.id)
    # create each field with the offer id
    for field_id, value in values['fields'].items():
        if not value:
            continue
        field_id = int(field_id)
        print(field_id, value, offer.id)
        print(type(field_id), type(value), type(offer.id))
        field = await Field.get(field_id, db)
        print(field.type_id, INT_TYPES)
        if field.type_id in INT_TYPES:
            print("INT_TYPES")
            await ValueInt.add(ValueInt(value=int(value), offer_id=offer.id, field_id=field_id), db)
        elif field.type_id in STRING_TYPES:
            print("STRING_TYPES")
            await ValueString.add(ValueString(value=value, offer_id=offer.id, field_id=field_id), db)
        elif field.type_id in FLOAT_TYPES:
            print("FLOAT_TYPES")
            await ValueFloat.add(ValueFloat(value=float(value), offer_id=offer.id, field_id=field_id), db)
            print("after add")
        elif field.type_id in BOOL_TYPES:
            print("BOOL_TYPES")
            await ValueBool.add(ValueBool(value=bool(int(value)), offer_id=offer.id, field_id=field_id), db)
    return offer


@router.get("", response_model=list[Offer])
async def get_offers(db: Session = Depends(get_db)):
    """Get a list of all offers."""
    return await Offer.get_all(db)

@router.get("/product/{id}", response_model=list[Offer])
async def get_offers(id: int, db: Session = Depends(get_db)):
    """Get a list of all offers."""
    return await Offer.get_by_product_id(id, db)

@router.get("/product/{id}/details")
async def get_offers(id: int, db: Session = Depends(get_db)):
    """Get a list of all offers."""
    offers = await Offer.get_by_product_id(id, db)
    offers = [model_to_dict(offer) for offer in offers]
    for offer in offers:
        fields = await ProductField.get_by_product_id(offer['product_id'], db)
        fields = {f"{model_to_dict(field)['field_id']}":None for field in fields}
        values_tables = [ValueBool, ValueFloat, ValueInt, ValueString]
        for table in values_tables:
            for value in await table.get_by_offer_id(offer['id'], db):
                value = model_to_dict(value, exclude=['offer_id'])
                field_id = value['field_id']
                field = model_to_dict(await Field.get(field_id, db))
                if field['type_id'] == 8:
                    value = model_to_dict(await Selection.get(value['value'], db))
                    fields[field_id] = value['name']
                    continue
                fields[field_id] = value['value']
        
        offer['fields'] = fields
        offer['username'] = model_to_dict(await User.get(offer['owner_id'], db))['username']

    return offers


@router.get("/{id}", response_model=Offer)
async def get_offer_id(id: int, db: Session = Depends(get_db)):
    """Get a offer by id."""
    offer = await Offer.get(id, db)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offer with that id was found.")

    return offer

@router.put("/{id}", response_model=Offer, dependencies=[Depends(JWTBearer(role="User"))])
async def update_offer(id: int, offer: Offer, db: Session = Depends(get_db)):
    """Update a offer."""
    offer = offer.dict()
    offer.pop('id')
    return await Offer.update(id, db, **offer)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(role="User"))])
async def delete_offer(id: int, db: Session = Depends(get_db)):
    """Delete a offer."""
    offer = await Offer.get(id, db)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offer with that id was found.")

    await Offer.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
