from datalayer.database_manager import DatabaseManager

class ProjectType:
    def __init__(self, name):
        self.name = name 
 
class ProjectTypesTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_projects_types(self):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM project_types")
                project_types = cur.fetchall()
        if project_types:
            return project_types
        else:
            return None
  
db_manager = DatabaseManager()
user_table = ProjectTypesTable(db_manager)