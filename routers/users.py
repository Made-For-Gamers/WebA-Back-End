import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from datalayer.database import Base, engine, Team, User
from base.base_response import Result
from authentication.auth_handler import signJWT
from jose import JWTError, jwt
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserLoginSchema(BaseModel):
    email: str 
    password: str 
    name: str | None = None
  
class UserInDB(User):
    password_hash: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")    

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)
 
def get_password_hash(password):
    return pwd_context.hash(password)
  
def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(email: str):
    session = Session(bind=engine, expire_on_commit=False) 
    user_data = session.query(User).filter(User.email.like(email))

    if(user_data is not None): 
        return UserInDB(**user_data)

def authenticate_user( email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(form_data.username, form_data.password) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
 
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

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user