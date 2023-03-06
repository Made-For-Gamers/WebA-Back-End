from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
from typing import List
from sqlalchemy.orm import Session
from base.base_response import Result
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings
from datalayer.repositories.user_repo import Users, UsersTable, db_manager

