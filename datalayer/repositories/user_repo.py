
from datalayer.database_manager import DatabaseManager


class Users:
    def __init__(self, id, name, email, password_hash, is_active, team_name=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.team_name = team_name
         
class UsersTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_user_by_email(self, email):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, password_hash, is_active, team_name FROM Users WHERE is_active = true AND email = %s", (email,))
                user = cur.fetchone()
        if user:
            return Users(*user)
        else:
            return None

    def add_update_user(self, user):
        res = False
        with self.db_manager as conn:
         with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE is_active = true AND email = %s", (user.email,))
            row = cur.fetchone()
            
            if row is None:
                cur.execute("INSERT INTO users (email, name, password_hash, is_active, team_name) VALUES (%s, %s, %s, %s, %s)",
                               (user.email, user.name, user.password_hash, True, user.team_name))
                res = True
            else:
                cur.execute("UPDATE users SET email = %s, name = %s, is_active = %s, team_name = %s WHERE email = %s",
                               (user.email, user.name, user.is_active, user.team_name))
                res = False
        return res
 
db_manager = DatabaseManager()
user_table = UsersTable(db_manager)