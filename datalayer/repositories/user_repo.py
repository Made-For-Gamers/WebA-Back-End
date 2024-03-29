
from datalayer.database_manager import DatabaseManager
import random

class Users:
    def __init__(self, id, name, email, password_hash, is_active, surname=None, team_name=None, wallet_addr=None, profile_pic=None, extra_arg=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash 
        self.is_active = is_active
        self.team_name = team_name
        self.wallet_addr = wallet_addr 
        self.profile_pic = profile_pic 
        self.surname = surname
 
class UsersTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager

    def get_user_by_email(self, email):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, password_hash, is_active, surname, team_name, wallet_address, profile_pic FROM users WHERE is_active = true AND email = %s", (email,))
                user = cur.fetchone()
        if user:
            return Users(*user)
        else:
            return None

        
    def get_or_create_user_w3(self, wallet_address): 
        with self.db_manager as conn:
         with conn.cursor() as cur: 
            cur.execute("SELECT * FROM users WHERE is_active = true AND wallet_address = %s", (wallet_address,))
            row = cur.fetchone()  
            if row is not None:   
                return Users(*row) 
            else: 
                email = "Anonymous@" + wallet_address + ".com"
                password_hash = random.getrandbits(128)

                cur.execute("INSERT INTO users (email, name, password_hash, is_active, team_name, wallet_address) VALUES (%s, %s, %s, %s, %s, %s)",
                                 (email, wallet_address, password_hash, True, None, wallet_address))
                conn.commit()  # Commit the transaction

                cur.execute("SELECT * FROM users WHERE is_active = true AND wallet_address = %s", (wallet_address,))
                newUser = cur.fetchone() 
                if newUser:
                    return Users(*newUser)
                else:
                    return None
         
    def update_profile_pic(self, email, profile_pic):
        res = False
        with self.db_manager as conn:
         with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE is_active = true AND email = %s", (email,))
            row = cur.fetchone() 
            if row is None: 
                res = False
            else:
                cur.execute("UPDATE users SET profile_pic = %s WHERE email = %s",
                               (profile_pic, email))
                res = True
        return res

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