from typing import Optional
from pydantic import BaseModel
from datalayer.database_manager import DatabaseManager


class ProjectFeatureModel(BaseModel):
    id : Optional[int] = None 
    project_id: Optional[int] = None 
    feature_id: Optional[int] = None 
    is_active: Optional[bool] = None 

class FeatureDict(BaseModel):
    values: dict[str, ProjectFeatureModel]
class ProjectFeatureTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_project_feature(self, project_id):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT" +
                    "  project_features.id, project_features.project_id, project_features.feature_id , project_features.is_active, " +
                    "  features.name, features.description, features.feature_image_url, features.supported_engines, features.documentation_url, features.web_url, features.git_url, features.feature_type, features.api_key, features.is_live, features.is_verified " +
                    "FROM project_features " +
                    "  LEFT JOIN features ON feature_id = features.id " +
                    "WHERE project_features.is_active = true AND project_features.project_id = %s", (project_id,))
                rows = cur.fetchall()
                project_types = []
                for row in rows:
                    project_dict = {
                        "id" : row[0],
                        "project_id" : row[1],
                        "feature_id" : row[2],
                        "is_active" : row[3], 
                        "name" : row[4],
                        "description" : row[5],
                        "feature_image_url" : row[6],
                        "supported_engines" : row[7],
                        "documentation_url" : row[8],
                        "web_url" : row[9],
                        "git_url" : row[10],
                        "feature_type" : row[11],
                        "api_key" : row[12],
                        "is_live" : row[13],
                        "is_verified" : row[14],
                    }
                    project_types.append(project_dict) 
                if project_types:
                    return project_types
                else:
                    return None

    def create_project_feature(self, project):
      with self.db_manager as conn:
          with conn.cursor() as cur:
              cur.execute("INSERT INTO project_features (project_id, feature_id) VALUES (%s, %s)",
                              (project.project_id, project.feature_id))
              cur.execute(
                  "SELECT * FROM project_features WHERE is_active = True AND project_id = %s", (project.project_id,))
              projects = cur.fetchall()
      if projects:
          return projects
      else:
          return None

    def delete_project_feature(self, project):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE project_features SET is_active = %s WHERE project_id = %s",
                            (project.is_active, project.project_id))
                return True

db_manager = DatabaseManager()
user_table = ProjectFeatureTable(db_manager)