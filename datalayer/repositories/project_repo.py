from datalayer.database_manager import DatabaseManager


class Project:
    def __init__(self, name, owner_email, project_type, is_active):
        self.name = name
        self.owner_email = owner_email
        self.project_type = project_type
        self.is_active = is_active


class ProjectsTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_projects_by_owner_email(self, email):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM projects WHERE is_active = True AND owner_email = %s", (email,))
                projects = cur.fetchall()
        if projects:
            return projects
        else:
            return None

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
                            (project.name, project.project_types, project.is_active))
                projects = cur.fetchone()
        if projects:
            return projects
        else:
            return None
 
db_manager = DatabaseManager()
user_table = ProjectsTable(db_manager)