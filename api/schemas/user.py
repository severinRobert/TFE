from typing import Optional

from models import Users
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
import random
import hashlib


class User(BaseModel):
    id: Optional[int]
    username: constr(max_length=40)
    email: constr(max_length=40)
    password: constr(max_length=500)
    salt: Optional[constr(max_length=40)]
    states_id: Optional[int]

    class Config:
        orm_mode = True

    @classmethod
    async def register(cls, user: 'User', db: Session) -> Optional['user']:
        """
        Add a user to the database.
        """
        # Check if the user already exists by email or name.
        if db.query(Users).filter(Users.email == user.email).first() or db.query(Users).filter(Users.username == user.username).first():
            print("User already exists")
            return 

        # generate salt
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salt = ''.join(random.choice(ALPHABET) for i in range(16))
        # hash the password
        hashed_password = hashlib.sha256(f'{user.password}{salt}'.encode('utf-8')).hexdigest()
        # store the salt and the hashed password in the database
        values = dict(user)
        values.pop('id')
        values['password'] = hashed_password
        values['salt'] = salt

        user = Users(**values)
        db.add(user)
        db.commit()
        
        return user
    
    @classmethod
    async def login(cls, given_user, db: Session) -> Optional['user']:
        """Check the login of a user."""
        user = db.query(Users).filter(Users.username == given_user.username).first() or db.query(Users).filter(Users.email == given_user.email).first()
        if not user:
            print("User does not exist")
            return
        # hash the password
        hashed_password = hashlib.sha256(f'{given_user.password}{user.salt}'.encode('utf-8')).hexdigest()
        if not hashed_password == user.password:
            print("Password is not correct")
            return
        return user

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['user']:
        """Get a user from the database from its id."""
        user = db.query(Users).filter(Users.id == id).first()
        return user

    @classmethod
    async def get_all(cls, db: Session) -> list['user']:
        """Return a list of all Users from the database."""
        return db.query(Users).all()

    @classmethod
    async def update(cls, id: int, db: Session, **kwargs) -> Optional['user']:
        """Update users of a user."""
        user = await cls.get(id, db)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.commit()
        return user

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['user']:
        """Delete a user and return it. Return None if the user does not exists."""
        user = await cls.get(id, db)
        if user:
            print("Deleting user")
            db.delete(user)
            db.commit()
        return user
