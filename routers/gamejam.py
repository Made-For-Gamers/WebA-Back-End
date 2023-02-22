from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from datalayer.database import Base, engine, Team, User
from base.base_response import Result

router = APIRouter()

router = APIRouter(
    prefix="/gamejam",
    tags=["gamejam"], 
    responses={404: {"description": "Not found"}},
)

class TeamMember(BaseModel):
    name: str
    email: str

class RegisterTeam(BaseModel):
    name: str
    members: List[TeamMember]

@router.post("/new_team", tags=["gamejam"])
async def add_new_team(data: RegisterTeam): 
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