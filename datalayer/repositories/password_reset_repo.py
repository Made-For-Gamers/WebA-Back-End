import datetime
from pydantic import BaseModel
from datalayer.database_manager import DatabaseManager
 
class PasswordResetToken(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime.datetime


class PasswordReset:
    def __init__(self, id, user_id, token, expires_at):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at 

class PasswordResetTable:
    def __init__(self, db_manager):
      self.db_manager = db_manager  

    def create_password_reset_token(self, user_id, token, expires_at):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                expires_at = datetime.datetime.fromtimestamp(expires_at)
                cur.execute("INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
                                (user_id, token, expires_at))

    def get_password_reset_token_by_user_id(self, email):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM password_reset_tokens WHERE user_id = (SELECT id FROM users WHERE email =  %s) ", (email,))
                row = cur.fetchone()
                if row is None:
                    return None
                row_dict = dict(zip([col.name for col in cur.description], row))  # convert the tuple to a dictionary
                return PasswordResetToken(**row_dict)

    def delete_token_by_id(self, reset_token_id):
        with self.db_manager as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM password_reset_tokens WHERE id = %s", (reset_token_id,))

db_manager = DatabaseManager()
user_table = PasswordResetTable(db_manager)