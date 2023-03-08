from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
from typing import Dict, List 
from base.base_response import Result, ResultList
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings
from datalayer.repositories.password_reset_repo import PasswordResetTable
from datalayer.repositories.user_repo import Users, UsersTable, db_manager
from services.email.email_server_service import EmailModel, EmailServer
 
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
 
class UserPartialSchema(BaseModel):
    email: str
    password: str
    name: str | None = None 

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoggedIn(BaseModel):
    email: str 
    name: str | None = None
    team_name: str | None = None
    is_active : bool | None = None
 
class UserInDB(Users):
    password_hash: str
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
 
def delete_password_reset_token(reset_token_id):
     with db_manager as db:
         pwr_table = PasswordResetTable(db)
         pwr_table.delete_token_by_id(reset_token_id)

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)
 
def get_password_hash(password):
    return pwd_context.hash(password)

def update_user_password(email, password):
     with db_manager as db:
        user_table = UsersTable(db)
        return user_table.update_user_password(email=email, password=password)

def send_password_reset_email(email: str, token: str):
    sender_name = "noreply@mfg.gg"
    emailer = EmailServer(sender_name)
    reset_url = f"http://localhost:8000/reset-password?token={token}"
    receiver_name = ""
    receiver_email = email
    email_body = f'''Click the link below to reset your password:\n{reset_url}'''
    email_model = EmailModel(receiver_name, receiver_email, email_body, "MFG Password Reset Request", "Password Reset")
   
    emailer.send_mail(email_model)
    return True

def generate_password_reset_token(email: str) ->str:
    user = get_user(email=email)
    if user is None:
        return Result(result=False, message="User Not Found")
    token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=24)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    with db_manager as db:
        pwr_table = PasswordResetTable(db)
        pwr_table.create_password_reset_token(user.id, token, token_data["exp"])
        send_password_reset_email(email, token)
  
def get_user(email: str):
    with db_manager as db:
        user_table = UsersTable(db)
        user_data = user_table.get_user_by_email(email)

    if (user_data is not None): 
        return user_data
 
def authenticate_user(email: str, password: str):
    with db_manager as db:
        user_table = UsersTable(db)
        user = user_table.get_user_by_email(email) 
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("sub")
        if email  is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Users = Depends(get_current_user)):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

 
@router.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"result": True, "access_token": access_token, "token_type": "bearer"}

@router.post('/forgot-password')
async def forgot_password(email: str):
    generate_password_reset_token(email)
    return Result(result=True, message="Password reset email sent")

@router.get("/reset-password")
async def reset_password(token: str, new_password: str):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = token_data["sub"]
        expires_at = datetime.utcfromtimestamp(token_data["exp"])

        with db_manager as db:
            pwr_table = PasswordResetTable(db)
            reset_token = pwr_table.get_password_reset_token_by_user_id(email=email) 
            if reset_token is None:
                return Result(result=False, message="Password reset token not found") 
            if reset_token.token != token:
                return Result(result=False, message="Invalid password reset token")  
            if datetime.utcnow() > expires_at:
                return Result(result=False, message="Password reset token has expired") 
            update_user_password(email, new_password)
            delete_password_reset_token(reset_token.id)
        return {"message": "Password reset successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password reset token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password reset token")

 
@router.post('/signup', tags=["users"])
async def signup(user: UserPartialSchema):
    with db_manager as db:
        resMsg = "" 
        try:
            validation = validate_email(user.email)
            user.email = validation.email
        except EmailNotValidError as e:
            return Result(result=False, message=f"Invalid email: {user.email}")

        user_table = UsersTable(db)
        user.password = get_password_hash(user.password)
        userModel = Users(id=None, is_active=True, name=user.name, email=user.email,
                          password_hash=user.password)
        res = user_table.add_update_user(userModel)

        if res is True:
         resMsg = "User has been registered."
        else:
         resMsg = "User already exists."
    return Result(result=res, message=resMsg)

@router.get("/users/me", tags=["users"])
async def read_user(current_user: UserLoggedIn= Depends(get_current_active_user)):
    current_user.password_hash = 'PROTECTED'
    return ResultList(result=True, message="User Retrieved", body=current_user) 
