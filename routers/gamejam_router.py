from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List 
from base.base_response import Result
from datalayer.repositories.team_repo import TeamsTable
from datalayer.repositories.user_repo import Users, UsersTable, db_manager
from email_validator import validate_email, EmailNotValidError

from services.email.email_server_service import EmailModel, EmailServer

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

def send_game_jam_welcome_mail(name, email):
    sender_name = "MFG GameJam Wizzard"
    emailer = EmailServer(sender_name)
 
    receiver_name = name
    receiver_email = email
    email_body = ""
    email_model = EmailModel(receiver_name, receiver_email, email_body, "You Shall Pass! Welcome to the 2023 Game Jam!", "Demo Msg")
    html_template_name = "gamejam_welcome.html"
    
    emailer.send_html_mail(email_model, html_template_name)
    return True


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
            try:
                validation = validate_email(new_user.email)
                new_user.email = validation.email
            except EmailNotValidError as e:
                 return Result(result=False, message=f"Invalid email: {new_user.email}")
            
            user_exists = user_table.get_user_by_email(new_user.email) is not None
            if(user_exists):
                return Result(result=False, message=f"User {new_user.email} already exists")

        for new_user in data.members:
            user = Users(id=None, is_active=True, name=new_user.name, email=new_user.email, password_hash="", team_name=data.team_name)
            user_table.add_update_user(user)
            send_game_jam_welcome_mail(user.email)
    
    return Result(result=True, message="Created the team successfully")