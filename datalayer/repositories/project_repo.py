from typing import Optional
from pydantic import BaseModel
from datalayer.database_manager import DatabaseManager
 
class Project:
    def __init__(self, name, owner_email, project_type, is_active):
        self.name = name
        self.owner_email = owner_email
        self.project_type = project_type
        self.is_active = is_active

class ProjectModel(BaseModel):
    id : int
    name: Optional[str] = None
    owner_email: Optional[str] = None
    project_types: Optional[str] = None
    is_active: Optional[bool] = None 

class ProjectDict(BaseModel):
    values: dict[str, ProjectModel]
 
class ProjectsTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_projects_by_owner_email(self, email):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM projects WHERE is_active = True AND owner_email = %s", (email,))
                rows = cur.fetchall()
                projects = []
                for row in rows:  
                    project_dict = {
                        "id" : row[0],
                        "name": row[1],
                        "project_types": row[2],
                        "is_active": row[3],
                        "owner_email": row[4], 
                    }  
                    projects.append(project_dict)
                return projects

    def create_project(self, project):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO projects (name, project_types, is_active, owner_email) VALUES (%s, %s, %s, %s)",
                                (project.name, project.project_types, True, project.owner_email))
                cur.execute(
                    "SELECT * FROM projects WHERE is_active = True AND owner_email = %s", (project.owner_email,))
                projects = cur.fetchall()
        if projects:
            return projects
        else:
            return None

    def update_project_by_id(self, project):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE projects SET name = %s, project_types = %s, is_active = %s WHERE id = %s",
                            (project.name, project.project_types, project.is_active, project.id))
                cur.execute(
                    "SELECT * FROM projects WHERE id = %s", (project.id,))
                projects = cur.fetchone()
        if projects:
            return projects
        else:
            return None
 
db_manager = DatabaseManager()
user_table = ProjectsTable(db_manager)