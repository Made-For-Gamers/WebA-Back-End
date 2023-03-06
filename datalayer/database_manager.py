import psycopg2
from config import settings

class DatabaseManager:
    def __init__(self):
        self.connection = None
    
    def __enter__(self):
        self.connection = psycopg2.connect(
            host=settings.POSTGRES_HOSTNAME,
            port=settings.DATABASE_PORT,
            database= settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

 