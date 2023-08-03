from schemas import Selection, SelectionsGroup
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from utils import model_to_dict


router = APIRouter(
    prefix="/selections_groups",
    tags=["selections_groups"],
)

@router.post("", response_model=SelectionsGroup, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_selections_group(selections_group: SelectionsGroup, db: Session = Depends(get_db)):
    """Add a selections_group."""
    if await SelectionsGroup.get_by_name(selections_group.name, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A selections_group with that name already exists.")
    return await SelectionsGroup.add(selections_group, db)

@router.get("", response_model=list[SelectionsGroup])
async def get_selections_groups(db: Session = Depends(get_db)):
    """Get a list of all selections_groups."""
    return await SelectionsGroup.get_all(db)

@router.get("/details")
async def get_selections_groups(db: Session = Depends(get_db)):
    """Get a list of all selections_groups."""
    selections_groups = await SelectionsGroup.get_all(db)
    selections_groups = [model_to_dict(selections_group) for selections_group in selections_groups]
    for selections_group in selections_groups:
        selections = await Selection.get_by_selections_groups_id(selections_group['id'], db)
        selections = [model_to_dict(selection, exclude=['selections_groups_id']) for selection in selections]
        # add selections to selections_group
        selections_group['selections'] = selections
    return selections_groups

@router.get("/{id}", response_model=SelectionsGroup)
async def get_selections_group_id(id: int, db: Session = Depends(get_db)):
    """Get a selections_group by id."""
    selections_group = await SelectionsGroup.get(id, db)
    if not selections_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No selections_group with that id was found.")

    return selections_group

@router.get("/{id}/details")
async def get_selections_group_details(id: int, db: Session = Depends(get_db)):
    """Get a selections_group by id."""
    selections_group = await SelectionsGroup.get(id, db)
    if not selections_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No selections_group with that id was found.")

    selections = await Selection.get_by_selections_groups_id(id, db)

    selections_group = model_to_dict(selections_group)
    selections = [model_to_dict(selection, exclude=['selections_groups_id']) for selection in selections]
    # add selections to selections_group
    selections_group['selections'] = selections
    print(selections_group)
    return selections_group

@router.get("/{id}/selections")
async def get_selections_group_selections(id: int, db: Session = Depends(get_db)):
    """Get a selections_group by id."""
    selections_group = await SelectionsGroup.get(id, db)
    if not selections_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No selections_group with that id was found.")

    selections = await Selection.get_by_selections_groups_id(id, db)

    return selections

@router.put("/{id}", response_model=SelectionsGroup, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def update_selections_group(id: int, selections_group: dict[str, str], db: Session = Depends(get_db)):
    """Update a selections_group and return it. Return None if the selections_group does not exists."""
    db_selections_group = await SelectionsGroup.update(id, selections_group, db)
    if not db_selections_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No selections_group with that id was found.")
    return db_selections_group

@router.delete("/{id}", response_model=SelectionsGroup, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def delete_selections_group(id: int, force: bool = False, db: Session = Depends(get_db)):
    """Delete a selections_group and return it. Return None if the selections_group does not exists."""
    try:
        await SelectionsGroup.delete(id, db, force)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
