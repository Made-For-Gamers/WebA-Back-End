
from datalayer.database_manager import DatabaseManager


class Users:
    def __init__(self, id, name, email, password_hash, is_active, team_name=None, wallet_addr=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.team_name = team_name
        self.wallet_addr = wallet_addr
 
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
        
    def get_or_create_user_w3(self, user): 
        with self.db_manager as conn:
         with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE is_active = true AND wallet_addr = %s", (user.wallet_addr,))
            row = cur.fetchone()

            if row is None:  
                if(user.name is None):
                    user.name = "Anonymous"
                if(user.email is None):
                    user.email = "Anonymous@" + user.wallet_addr + ".com"

                cur.execute("INSERT INTO users (email, name, password_hash, is_active, team_name, wallet_addr) VALUES (%s, %s, %s, %s, %s, %s)",
                                 (user.email, user.name, user.password_hash, True, user.team_name, user.wallet_addr))
                newUser = cur.fetchone()
                if newUser:
                    return Users(*newUser)
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
    
    def update_user_password(self, email, password):
        res = False
        with self.db_manager as conn:
         with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE is_active = true AND email = %s", (email,))
            row = cur.fetchone() 
            if row is None: 
                res = False
            else:
                cur.execute("UPDATE users SET password_hash = %s WHERE email = %s",
                               (password, email))
                res = True
        return res
 
db_manager = DatabaseManager()
user_table = UsersTable(db_manager)