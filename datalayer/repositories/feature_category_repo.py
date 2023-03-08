from datalayer.database_manager import DatabaseManager

class FeatureCategory:
    def __init__(self, name):
        self.name = name 
 
class FeatureCategoriesTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_feature_categories(self):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM feature_categories WHERE is_active = true")
                rows = cur.fetchall()
                project_types = []
                for row in rows:
                    project_dict = {
                        "id" : row[0],
                        "name" : row[1]
                    }
                    project_types.append(project_dict) 
            if project_types:
                return project_types
            else:
                return None
  
db_manager = DatabaseManager()
user_table = FeatureCategoriesTable(db_manager)