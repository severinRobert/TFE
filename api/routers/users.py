from datetime import timedelta

from schemas import User, Role
from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel
from database import get_db
from auth import create_access_token, get_payload

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

def get_current_token():
    """Get current token."""
    return "token"

def is_request_owner(request: Request, user_id: int):
    """Check if token is owner."""
    print(request.headers.get("authorization"))
    if request.headers.get("authorization"):
        token = request.headers.get("authorization").split(" ")[1]
        print(token)
        payload = get_payload(token)
        print(payload, user_id)
        return False if not payload else payload['user_id'] == int(user_id)
    return False

@router.post("/register", response_model=Token)
async def register_user(user: dict[str,str], db: Session = Depends(get_db)):
    """Register a user."""
    user = await User.register(User(**user), db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or username already exists.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(user.roles_id)
    role = await Role.get(user.roles_id, db)
    print(role)
    access_token = create_access_token(
        data={"sub": user.username, "role": role.name, "user_id": user.id}, expires_delta=access_token_expires
    )    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login a user."""
    user = await User.login(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    role = await Role.get(user.roles_id, db)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": role.name, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{id}/profile")
async def user_profile(id: int, request: Request, db: Session = Depends(get_db)):
    """Get user details for profile."""
    with_details = is_request_owner(request, id)

    profile = {'id': id}
    user = await User.get(id, db)
    print(user)
    print(user.username)
    profile['username'] = user.username
    profile['contact'] = user.contact
    if with_details:
        profile['email'] = user.email
        profile['roles_id'] = user.roles_id
        profile['roles_name'] = (await Role.get(user.roles_id, db)).name
    return profile

@router.put("/{id}")
async def user_profile(id: int, details: dict[str,str|dict], request: Request, db: Session = Depends(get_db)):
    """Update user details."""
    print(id, details)
    profile = details['profile']
    password = details['password']

    user = await User.login(profile["username"], password, db)
    print(user, is_request_owner(request, id))
    if not user or not is_request_owner(request, id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    print(user)
    print(user.username)
    return await User.update(user.id, profile, db)

@router.get("/me")
async def read_users_me(request: Request, db: Session = Depends(get_db)):
    """Get current user."""
    token = request.headers.get("authorization").split(" ")[1]
    payload = get_payload(token)
    response = {
        'id': payload['user_id'],
        'role': payload['role']
    }
    return response

