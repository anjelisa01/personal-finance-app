#contain security auth

from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#--------------------------sign up-------------------------------
#hash password
def hash_password(password:str):
    return pwd_context.hash(password)

#--------------------------log in--------------------------------
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
def get_user_by_email(db:Session,email:str):
    stmt=select(User).where(User.email==email)
    return db.scalars(stmt).first()

#verify password
def verify_password(db:Session,password:str,hashed_password:str):
    return pwd_context.verify(password,hashed_password)

#--------------------------JWT creation----------------------------
from jose import jwt,JWTError
from datetime import datetime,timedelta
import os 
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=30)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm='HS256')