from datalayer.repositories.project_features_repo import ProjectFeatureModel, ProjectFeatureTable
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from base.base_response import Result, ResultList
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datalayer.repositories.user_repo import db_manager
from routers.user_router import UserLoggedIn, get_current_active_user


router = APIRouter()

router = APIRouter(
    prefix="/project_feature",
    tags=["project_feature"],
    responses={404: {"description": "Not found"}},
)

@router.get("/me", tags=["project_feature"], summary="Gets project_features")
async def read_project_feature(project_id: int, current_user: UserLoggedIn= Depends(get_current_active_user)):
    with db_manager as db:
        project_table = ProjectFeatureTable(db)
        project_dict = project_table.get_project_feature(project_id)
    return ResultList(result=True, message="Project features retrieved", body=project_dict)

@router.post("/link", tags=["project_feature"], summary="Links feature to project")
async def write_project_feature(project_feature: ProjectFeatureModel, current_user: UserLoggedIn= Depends(get_current_active_user)):
    with db_manager as db:
        project_table = ProjectFeatureTable(db)
        project_dict = project_table.create_project_feature(project_feature)
    return ResultList(result=True, message="Project linked successfully", body=project_dict)
