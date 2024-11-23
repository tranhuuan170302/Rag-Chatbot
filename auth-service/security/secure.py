from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi.security import HTTPDigest, HTTPBasic
from models.data.sqlalchemy_models import Login
from secrets import compare_digest
from base64 import standard_b64decode
import os
from configparser import ConfigParser
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

http_basic = HTTPBasic()

crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
SECRET_KEY = "nzTwm8FTuuJ49k+JmXZdheLJfGVL3sNvC4BZHUW/5SkC87DeVnItpD2nzoWjq4xU"
ALGORITHM="HS256"

def get_password_hash(password):
    return crypt_context.hash(password)

def build_map():
    env = os.getenv("ENV", ".config")
    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["CREDENTIALS"]
    else:
        config = {
            "USERNAME": os.getenv("USERNAME", "guest"),
            "PASSWORD": os.getenv("PASSWORD", "guest"),
            
        }
    return config

http_digest = HTTPDigest()

def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def authenticate(credentials: HTTPAuthorizationCredentials, account: Login):
    try:
        is_email = compare_digest(credentials.username, account.email)
        is_password = compare_digest(credentials.password, account.password)
        verified_password = verify_password(credentials.password, account.passphrase)
        return (verified_password and is_email and is_password)
    except Exception as e:
        print(e)
        return False

def verified_password(password, account: Login):
    try:
        is_password = compare_digest(password, account.password)
        verified_password = verify_password(password, account.passphrase)
        return (verified_password and is_password)
    except Exception as e:
        print(e)
        return False
    
def create_access_token(data: dict, expires_after: timedelta):
    plain_text = data.copy()
    expire = datetime.utcnow() + expires_after
    plain_text.update({"exp": expire})
    encoded_jwt = jwt.encode(plain_text, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt