from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Team(Base):
    __tablename__ = 'Teams'
    Name = Column(String(256),primary_key=True)
    Members: Mapped[List["User"]] = relationship(back_populates="Team")

class User(Base):
    __tablename__ = 'Users'
    Name = Column(String, nullable=False)
    Email = Column(String, primary_key=True)
    PasswordHash = Column(String, nullable=False)
    Team = relationship("Team", back_populates="Members")
    Team_Name : Mapped[String] = mapped_column(ForeignKey("Teams.Name"),nullable=True)


