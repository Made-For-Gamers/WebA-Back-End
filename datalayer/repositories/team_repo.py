
from datalayer.database_manager import DatabaseManager


class Teams:
    def __init__(self, name):
        self.name = name
         
class TeamsTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_team_by_name(self, team_name):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM teams WHERE is_active = True AND name = %s", (team_name,))
                team = cur.fetchone()
        if team:
            return team
        else:
            return None
  
    def register_team(self, team_name):
        res = False
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM teams WHERE name = %s", (team_name,))
                row = cur.fetchone()
                if row is None:
                    cur.execute("INSERT INTO teams (name, is_active) VALUES (%s, %s)",
                                    (team_name, True))
                    res = True
                else:
                    res = False 
        return res
 
db_manager = DatabaseManager()
user_table = TeamsTable(db_manager)