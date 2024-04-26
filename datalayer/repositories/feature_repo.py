from pydantic import BaseModel
from datalayer.database_manager import DatabaseManager
from typing import List, Optional

class FeatureModel(BaseModel):
    id: Optional[int] = None 
    name: Optional[str] = None
    description: Optional[str] = None
    feature_image_url: Optional[str] = None
    supported_engines: Optional[List[str]] = None  
    documentation_url: Optional[str] = None
    web_url: Optional[str] = None
    git_url: Optional[str] = None
    feature_type: Optional[List[str]] = None  
    api_key: Optional[str] = None
    is_active: Optional[bool] = None 
    is_live: Optional[bool] = None  
    is_verified: Optional[bool] = None 
    project_id: int  

class FeatureDict(BaseModel):
    values: dict[str, FeatureModel]

 
class FeatureTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_feature_by_project_id(self, id):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM features WHERE is_active = True AND project_id = %s", (id,))
                rows = cur.fetchall()
                features = []
                for row in rows:
                    feature = FeatureModel(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        feature_image_url=row[3],
                        supported_engines=row[4],
                        documentation_url=row[5],
                        web_url=row[6],
                        git_url=row[7],
                        feature_type=row[8],
                        api_key=row[9],
                        is_active=row[10],
                        is_live=row[11],
                        is_verified=row[12],
                        project_id=row[13]
                    )
                    features.append(feature.dict()) 
                return features

    def get_all_features(self):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM features WHERE is_active = true AND is_live = true AND is_verified = true")
                rows = cur.fetchall()
                features = []
                for row in rows:
                    feature = FeatureModel(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        feature_image_url=row[3],
                        supported_engines=row[4],
                        documentation_url=row[5],
                        web_url=row[6],
                        git_url=row[7],
                        feature_type=row[8],
                        api_key=row[9],
                        is_active=row[10],
                        is_live=row[11],
                        is_verified=row[12],
                        project_id=row[13]
                    )
                    features.append(feature.dict()) 
                return features

    def create_feature(self, feature):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO features (name, description, feature_image_url, supported_engines, documentation_url, web_url, git_url, feature_type, api_key, is_active, is_live, is_verified, project_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (feature.name, feature.description, feature.feature_image_url, feature.supported_engines, feature.documentation_url, feature.web_url, feature.git_url, feature.feature_type, feature.api_key, feature.is_active, feature.is_live, feature.is_verified, feature.project_id))
                cur.execute(
                    "SELECT * FROM features WHERE is_active = True AND project_id = %s AND name = %s", (feature.project_id, feature.name,))
                res = cur.fetchone()
        if res:
            return res
        else:
            return None

    def update_project_by_id(self, feature):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE features SET name = %s, description=%s, feature_image_url=%s, supported_engines=%s, documentation_url=%s, web_url=%s, git_url=%s, feature_type=%s, api_key=%s, is_active=%s, is_live=%s, is_verified=%s WHERE id = %s",
                            (feature.name, feature.description, feature.feature_image_url, feature.supported_engines, feature.documentation_url, feature.web_url, feature.git_url, feature.feature_type, feature.api_key, feature.is_active, feature.is_live, feature.is_verified, feature.id))
                cur.execute(
                    "SELECT * FROM features WHERE id = %s", (feature.id,))
                res = cur.fetchone()
        if res:
            return res
        else:
            return None
 
db_manager = DatabaseManager()
user_table = FeatureTable(db_manager)