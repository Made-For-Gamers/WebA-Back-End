from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str
    SECRET: str
    ALGORITHM : str
    GMAILPASSWORD : str
    GMAILADDR : str
    CONTACTADDR : str
    RECAPTCHASECRET: str
    GCPPROJID: str

    class Config:
        env_file = './.env'


settings = Settings()