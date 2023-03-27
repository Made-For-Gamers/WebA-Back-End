from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from base.base_response import Result, ResultList
from datalayer.repositories.feature_category_repo import FeatureCategoriesTable
from datalayer.repositories.feature_repo import FeatureModel, FeatureTable  
from routers.user_router import UserLoggedIn, get_current_active_user
from datalayer.repositories.user_repo import db_manager

router = APIRouter()

router = APIRouter(
    prefix="/feature",
    tags=["feature"],
    responses={404: {"description": "Not found"}},
)

def get_feature_categories():
    with db_manager as db:
        feature_category_table = FeatureCategoriesTable(db)
        feature_categories = feature_category_table.get_feature_categories()
    return feature_categories

def get_features_for_project(project_id):
    with db_manager as db:
        feature_table = FeatureTable(db)
        features = feature_table.get_feature_by_project_id(project_id)
    return features

def get_all_features():
    with db_manager as db:
        feature_table = FeatureTable(db)
        features = feature_table.get_all_features()
    return features

def create_feature_func(feature):
    with db_manager as db:
        feature_table = FeatureTable(db)
        features = feature_table.create_feature(feature)
    return features

def update_feature_func(feature):
    with db_manager as db:
        feature_table = FeatureTable(db)
        features = feature_table.update_project_by_id(feature)
    return features

@router.get("/me", tags=["feature"], summary="Gets all features for selected project")
async def read_user(project_id: str, current_user: UserLoggedIn= Depends(get_current_active_user)): 
        res = get_features_for_project(project_id)
        return ResultList(result=True, message="Features Retrieved", body=res)

@router.get("/all", tags=["feature"], summary="Gets all live and verified features - for game projects to link to")
async def read_user(current_user: UserLoggedIn= Depends(get_current_active_user)): 
        res = get_all_features()
        return ResultList(result=True, message="Features Retrieved", body=res)

@router.get("/categories", tags=["feature"], summary="Gets all features categories")
async def read_user(current_user: UserLoggedIn= Depends(get_current_active_user)): 
        res = get_feature_categories()
        return ResultList(result=True, message="Feature Categories Retrieved", body=res)

@router.post("/create", tags=["feature"])
async def create_feature(feature: FeatureModel, current_user: UserLoggedIn= Depends(get_current_active_user)):
    res = create_feature_func(feature)
    if res is not None:
        return Result(result=True, message="Feature created successfully")
    else: 
        return Result(result=False, message="Feature could not be created")
    
@router.post("/update", tags=["feature"])
async def update_feature(feature: FeatureModel, current_user: UserLoggedIn= Depends(get_current_active_user)):
    res = update_feature_func(feature)
    if res is not None:
        return Result(result=True, message="Feature updated successfully")
    else: 
        return Result(result=False, message="Feature could not be created")