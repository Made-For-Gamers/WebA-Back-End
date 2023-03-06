from sqlalchemy import create_engine, Column, Boolean, String, ForeignKey
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
    name : Mapped[str] = mapped_column(String(256),primary_key=True)
    members: Mapped[List["User"]] = relationship(back_populates="Team")

class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] 
    name: Mapped[str] = mapped_column(String(256))
    email : Mapped[str] = mapped_column(primary_key=True)
    password_hash : Mapped[str] = mapped_column(String(256))
    is_active : Mapped[bool]
    team: Mapped["Team"] = relationship("Team", back_populates="members")
    team_Name : Mapped[String] = mapped_column(ForeignKey("Teams.name"),nullable=True)


