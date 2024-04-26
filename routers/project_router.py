from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from base.base_response import Result, ResultList
from datalayer.repositories.project_repo import ProjectsTable
from datalayer.repositories.project_type_repo import ProjectTypesTable
from datalayer.repositories.user_repo import Users, UsersTable, db_manager
from routers.user_router import UserLoggedIn, get_current_active_user
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/project",
    tags=["project"],
    responses={404: {"description": "Not found"}},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ProjectSchema(BaseModel):
    name: str
    project_types: str
    owner_email: str
    is_active: Optional[bool] = None 

class ProjectModel(BaseModel):
    name: str
    project_types: str

class ProjectUpdateModel(BaseModel):
    id: str
    name: str
    project_types: str
    is_active: bool

def get_current_user_projects(current_user_email):
    with db_manager as db:
        project_table = ProjectsTable(db)
        projects = project_table.get_projects_by_owner_email(current_user_email)
    return projects

def create_project_func(project):
    with db_manager as db:
        project_table = ProjectsTable(db)
        projects = project_table.create_project(project)
    return projects

def update_project_func(project):
    with db_manager as db:
        project_table = ProjectsTable(db)
        projects = project_table.update_project_by_id(project)
    return projects
  
@router.get("/me", tags=["project"], summary="Gets projects for logged in user")
async def read_user(current_user: UserLoggedIn = Depends(get_current_active_user)): 
    with db_manager as db:
        project_table = ProjectsTable(db) 
        project_dict = project_table.get_projects_by_owner_email(current_user.email) 
    return ResultList(result=True, message="Projects Retrieved", body=project_dict)

@router.post("/create", tags=["project"])
async def create_project(project: ProjectModel, current_user: UserLoggedIn = Depends(get_current_active_user)):
    projectModel = ProjectSchema(name=project.name, project_types=project.project_types, owner_email=current_user.email, is_active=True)
    projects = create_project_func(projectModel)
    if projects is not None:
        return Result(result=True, message="Project created successfully")
    else: 
        return Result(result=False, message="Project could not be created")
    
@router.post("/update", tags=["project"])
async def update_project(project: ProjectUpdateModel, current_user: UserLoggedIn = Depends(get_current_active_user)):
    projectModel = ProjectUpdateModel(id=project.id, name=project.name, project_types=project.project_types, owner_email=current_user.email, is_active=project.is_active)
    projects = update_project_func(projectModel)
    if projects is not None:
        return Result(result=True, message="Project updated successfully")
    else: 
        return Result(result=False, message="Project could not be updated")
    
@router.get("/types", tags=["project"], summary="Gets project types")
async def get_project_types(current_user: UserLoggedIn = Depends(get_current_active_user)):
    with db_manager as db:
         project_types_table = ProjectTypesTable(db)
         project_types_list = project_types_table.get_projects_types()
    return ResultList(result=True, message="Project Types Retrieved", body=project_types_list)
