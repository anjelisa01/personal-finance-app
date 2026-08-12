#import
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, UTC

#model and schema
from models.user import User
from schemas.user import UserCreate,UserUpdate 

#utils
from core.security import hash_password,get_user_by_email
from core.logger import logger
from core.exceptions import ResourceExistedError

class UserService:
    def __init__(self,db: Session):
        self.db = db

    def create(self, payload:UserCreate):
        #check existing user
        existing=get_user_by_email(self.db,payload.email)
        if existing:
            raise ResourceExistedError("User",payload.email)

        user=User(
            name=payload.name,
            email=payload.email,
            currency=payload.currency,
            hashed_password=hash_password(payload.password),
            deleted_at=None
        )
       
        #insert
        try:
            self.db.add(user)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 

        #logging important event
        logger.info("User created successfully, user_id=%s",user.id)
        self.db.refresh(user)
        return user
    
    def read_one(self,user_id:int):
        #no exception for if user existed or not, because user MUST existed to even access this service
        return self.db.scalar(
            select(User).where(User.id==user_id))

    def update(self,user_id:int,payload:UserUpdate):
        #find user
        user=self.db.scalar(
            select(User).where(User.id==user_id))
        #no exception for if user existed or not, because user MUST existed to even access this service

        #build the update data first, make sure if user changed password, hashed before commit
        update_data=payload.model_dump(exclude_unset=True)
        if "password" in update_data:
            user.hashed_password = hash_password(update_data.pop("password"))
        if "email" in update_data:
            existing=get_user_by_email(self.db,update_data["email"])
            if existing:
                raise ResourceExistedError("User",update_data["email"])

        #update
        try:
            for field,value in update_data.items():
                setattr(user,field,value)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        logger.info("User updated, user_id=%s", user_id)
        self.db.refresh(user)
        return user

    def delete(self,user_id:int):
        #find user
        user=self.db.scalar(
            select(User).where(User.id==user_id))
        #no exception for if user existed or not, because user MUST existed to even access this service

        #doing soft delete
        user.name=None
        user.email=None
        user.hashed_password=None
        user.deleted_at=datetime.now(UTC)

        #delete
        try:
            # self.db.delete(user)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("User deleted, user_id=%s", user_id)
        return{"message":"deleted"}