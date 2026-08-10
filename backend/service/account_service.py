#import
from sqlalchemy.orm import Session
from sqlalchemy import select

#model and schema
from models.account import Account
from schemas.account import AccountBase,AccountUpdate

#util
from core.logger import logger
from core.exceptions import ResourceExistedError,ResourceNotFoundError

def get_account_name(db:Session,user_id:int,account_name:str):
    stmt=select(Account).where(
        Account.user_id==user_id,
        Account.account_name==account_name)
    return db.scalars(stmt).first()

class AccountService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id
    def create(self,payload:AccountBase):
        #check existed account
        existing=get_account_name(self.db,self.user_id,payload.account_name)
        if existing:
            raise ResourceExistedError("Account",payload.account_name)

        #build goal data
        account=Account(**payload.model_dump())
        account.user_id=self.user_id

        #insert
        try:
            self.db.add(account)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 
        logger.info("New Account created, account id=%s",account.id)
        self.db.refresh(account)
        return account

    def read_one(self,account_id:int):
        #find account
        account=self.db.scalar(
        select(Account).where(
            Account.user_id==self.user_id,
            Account.id==account_id)
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)
        return account
        
    def read_all(self):
        return self.db.scalars(
            select(Account).where(Account.user_id == self.user_id)
        ).all()
        
    def update(self,account_id:int,payload:AccountUpdate):
        #find account
        account=self.db.scalar(
            select(Account).where(
                Account.user_id==self.user_id,
                Account.id==account_id))
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        #build update data
        update_data=payload.model_dump(exclude_unset=True)
        
        #if account_name existed in database
        if "account_name" in update_data:
            existing=get_account_name(self.db,self.user_id,update_data["account_name"])
            if existing:
                raise ResourceExistedError("Account",update_data["account_name"])

        #update
        try:
            for field,value in update_data.items():
                setattr(account,field,value)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Account updated, account id =%s", account_id)
        self.db.refresh(account)
        return account

    def delete(self,account_id:int):
        #find account
        account=self.db.scalar(
            select(Account).where(
                Account.user_id==self.user_id,
                Account.id==account_id))
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        #delete
        try:
            self.db.delete(account)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Account deleted.  Account id=%s", account_id) 
        return{"message":"deleted"}