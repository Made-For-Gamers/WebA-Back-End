from fastapi import FastAPI, HTTPException
from database import Base, engine, Team, User
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from auth_handler import signJWT
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

#https://testdriven.io/blog/fastapi-jwt-auth/

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

class TeamMember(BaseModel):
    name: str
    email: str

class RegisterTeam(BaseModel):
    name: str
    members: List[TeamMember]


class UserLoginSchema(BaseModel):
    email: str 
    password: str 
    name: str

class Result(BaseModel):
    result:str
    message:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create the database
Base.metadata.create_all(engine)



@app.get('/')
def index():
    return {":":")"}


@app.post('/new_team')
def add_new_team(data: RegisterTeam):
    # user_in_db = session.query(Team).first()
    session = Session(bind=engine, expire_on_commit=False)

    # check if there is a team already
    team_exists = session.query(Team).filter_by(
        Name=data.name).first() is not None

    if (not team_exists):
        # if the team is not taken create it
        team = Team(Name=data.name)
        session.add(team)

    #check if the users exist already
    for new_user in data.members:
        user_exists = session.query(User).filter_by(Email=new_user.email).first() is not None
        if(user_exists):
            raise HTTPException(status_code=400)
    
    for new_user in data.members:
        user = User(Name=new_user.name, Email=new_user.email, PasswordHash="", Team_Name=data.name)
        session.add(user)
    session.commit()
    session.close()
    return Result(result=True,message="Created the team succesfully")

@app.post('/login')
def login(user: UserLoginSchema):
    session = Session(bind=engine, expire_on_commit=False)

    pass_hash = get_password_hash(user.password)

    user_data = session.query(User).filter(User.Email.like(user.email),User.PasswordHash.like(pass_hash))
    
    if(user_data is not None):
        return signJWT(user.email)

    raise HTTPException(status_code=400)
 

@app.post('/signup')
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


