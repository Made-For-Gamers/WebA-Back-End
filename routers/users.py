from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from datalayer.database import Base, engine, Team, User
from base.base_response import Result
from authentication.auth_handler import signJWT
from passlib.context import CryptContext
from config import settings

# https://testdriven.io/blog/fastapi-jwt-auth/
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"], 
    responses={404: {"description": "Not found"}},
) 

class UserLoginSchema(BaseModel):
    email: str 
    password: str 
    name: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
 
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/login')
def login(user: UserLoginSchema):
    session = Session(bind=engine, expire_on_commit=False)

    pass_hash = get_password_hash(user.password)

    user_data = session.query(User).filter(User.Email.like(user.email),User.PasswordHash.like(pass_hash))
    
    if(user_data is not None):
        return signJWT(user.email)

    raise HTTPException(status_code=400)
  
@router.post('/signup')
def signup(user: UserLoginSchema):
    
    session = Session(bind=engine, expire_on_commit=False)

    user_doesnt_exist = session.query(User).filter_by(
        Email=user.email).first() is None
    if(user_doesnt_exist):

        user_data = User(Name = user.name,Email = user.email,PasswordHash = get_password_hash(user.password))
        session.add(user_data)
        session.commit()
        return signJWT(user.email)

    raise HTTPException(status_code=400)