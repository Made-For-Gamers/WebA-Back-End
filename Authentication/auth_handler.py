import time
from typing import Dict
from passlib.context import CryptContext
import jwt
from decouple import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 604800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def generate_reset_token():
    return jwt.encode({"reset": True}, JWT_SECRET, algorithm=JWT_ALGORITHM)