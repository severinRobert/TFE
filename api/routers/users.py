from schemas import User
from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register")
async def register_user(user: User, db: Session = Depends(get_db)):
    """Register a user."""
    if not await User.register(user, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or username already exists.")
    return Response(status_code=status.HTTP_201_CREATED, content="User created successfully.")

@router.post("/login")
async def login_user(user: User, db: Session = Depends(get_db)):
    """Login a user."""
    if not await User.login(user, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email/username or password does not exist.")
    return Response(status_code=status.HTTP_200_OK, content="User logged in successfully.")

