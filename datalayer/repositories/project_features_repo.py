from pydantic import BaseModel
from datalayer.database_manager import DatabaseManager

class ProjectFeatureTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

class ProjectFeatureModel(BaseModel):
    id : int
    project_id: int
    feature_id: int
    is_active: bool

    def get_project_feature(self, project_id):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM project_features WHERE is_active = true AND project_id = %s", (project_id,))
                rows = cur.fetchall()
                project_types = []
                for row in rows:
                    project_dict = {
                        "id" : row[0],
                        "project_id" : row[1],
                        "feature_id" : row[2],
                        "is_active" : row[3]
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