from schemas import State
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/states",
    tags=["states"],
)


@router.get("", response_model=list[State])
async def get_state(db: Session = Depends(get_db)):
    """Get a list of all state."""
    return await State.get_all(db)


@router.get("/{id}", response_model=State)
async def get_state_id(id: int, db: Session = Depends(get_db)):
    """Get a state by id."""
    state = await State.get(id, db)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No state with that id was found.")

    return state
