from schemas import Selection, ValueInt
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from utils import model_to_dict


router = APIRouter(
    prefix="/selections",
    tags=["selections"],
)

@router.post("", response_model=Selection, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_selections(selections: Selection, db: Session = Depends(get_db)):
    """Add a selections."""
    if await Selection.get_by_name(selections.name, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A selections with that name already exists.")
    return await Selection.add(selections, db)

async def detail_selection(details, db, schema):
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
            await schema.delete(id, db)
        elif detail['type'] == 'add':
            await schema.add(Selection(name=detail['name'], description=detail['description'], selections_groups_id=details['selections_groups_id']), db)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid type.")
    if to_verify:
        # raise error and send to_verfy to frontend
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="The selection is used in an offer.", 
                            headers={"to_verify": to_verify})

@router.post("/details", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_selection(details: dict[str, int | dict], db: Session = Depends(get_db)):
    return await detail_selection(details, db, Selection)

@router.get("", response_model=list[Selection])
async def get_selections(db: Session = Depends(get_db)):
    """Get a list of all selections."""
    return await Selection.get_all(db)

@router.get("/{id}", response_model=Selection)
async def get_selections_id(id: int, db: Session = Depends(get_db)):
    """Get a selections by id."""
    selections = await Selection.get(id, db)
    if not selections:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No selections with that id was found.")

    return selections

