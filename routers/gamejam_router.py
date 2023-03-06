from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List 
from base.base_response import Result
from datalayer.repositories.team_repo import TeamsTable
from datalayer.repositories.user_repo import Users, UsersTable, db_manager

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
    team_name: str
    members: List[TeamMember]

@router.post("/new_team", tags=["gamejam"])
async def add_new_team(data: RegisterTeam): 
    with db_manager as db:
        user_table = UsersTable(db)
        teams_table = TeamsTable(db)
  
        #check if the team name is already taken
        team_check = teams_table.get_team_by_name(data.team_name)

        if team_check is not None: 
            return Result(result=False, message="Team already exists")
        
        teams_table.register_team(data.team_name)

        #check if the users exist already
        for new_user in data.members:
            user_exists = user_table.get_user_by_email(new_user.email) is not None
            if(user_exists):
                return Result(result=False, message=f"User {new_user.email} already exists")

        for new_user in data.members:
            user = Users(id=None, is_active=True, name=new_user.name, email=new_user.email, password_hash="", team_name=data.team_name)
            user_table.add_update_user(user)
    
    return Result(result=True, message="Created the team successfully")