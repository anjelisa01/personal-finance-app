#import
from sqlalchemy.orm import Session
from sqlalchemy import select

#models and schemas
from models.transaction import Transaction 
from models.account import Account
from schemas.transaction import TransactionAdd,TransactionResponse,TransactionUpdate,Transfer

#util
from core.exceptions import ResourceExistedError,ResourceNotFoundError
from core.logger import logger


#transaction Transfer:
class TransferService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id

    def create_transfer(self,tr:Transfer,payload:TransactionAdd):
        transfer_data=tr.model_dump(exclude_unset=True)
        account_in=transfer_data['account_id_in']
        account_out=transfer_data['account_id_out']

        #outgoing account: build transaction data
        transaction=Transaction(**payload.model_dump())
        transaction.account_id= transfer_data['account_id_in']
        transaction.transaction_type='transfer'
        # transaction.transfer_id=
        transaction.transfer_direction='outgoing'    
        if transaction.category_id==0:
                transaction.category_id=None
                
        #insert
        try:
            self.db.add(transaction)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 
        logger.info("Transaction created, transaction id=%s", transaction.id)
        self.db.refresh(transaction)
        return transaction

        
        '''
        generate transfer_id
        transaction_type="transfer"
        add_transaction(account_id_in,transfer_id,transfer_direction='incoming',transaction_type)
        add_transaction(account_id_out,transfer_id,transfer_direction='outgoing',transaction_type)
        '''   

from sqlalchemy import text

class TransactionService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id

    def create_transfer(self,account_out:int,account_in:int,payload:TransactionAdd):

        #outgoing account: build transaction data
        out_transaction=Transaction(**payload.model_dump())
        out_transaction.account_id= account_out
        out_transaction.transaction_type='transfer'
        out_transaction.transfer_id = self.db.execute(
            text("SELECT nextval('transfer_id_seq')")
        ).scalar_one()
        out_transaction.transfer_direction='outgoing'   

        in_transaction=Transaction(**payload.model_dump())
        in_transaction.account_id= account_in
        in_transaction.transaction_type='transfer'
        in_transaction.transfer_id=out_transaction.transfer_id
        in_transaction.transfer_direction='incoming'  

        if out_transaction.category_id==0:
            out_transaction.category_id=None
            in_transaction.category_id=None
                
        #insert
        try:
            self.db.add_all([out_transaction,in_transaction])
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 

        return self.db.scalars( 
            select(Transaction).where(Transaction.transfer_id == out_transaction.transfer_id)
        ).all()
 
    def create(self,account_id:int,payload:TransactionAdd):
        #find account 
        account = (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == self.user_id,
            )
            .first()
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        #build transaction data
        transaction=Transaction(**payload.model_dump())
        transaction.account_id=account.id

        #update account balance
        # if transaction.transaction_type=="expense":
        #     account.current_balance=account.current_balance - transaction.amount
        # if transaction.transaction_type=="income":
        #     account.current_balance=account.current_balance + transaction.amount
       

        #if category not set, input null to db
        if transaction.category_id==0:
            transaction.category_id=None
            
        #insert
        try:
            self.db.add(transaction)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 
        logger.info("Transaction created, transaction id=%s", transaction.id)
        self.db.refresh(transaction)
        return transaction
    def read_one(self,account_id:int,transaction_id:int):
        #find account 
        account = (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == self.user_id,
            )
            .first()
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)
        
        # find the transaction
        transaction= self.db.scalar(
            select(Transaction).where(
                Transaction.account_id==account.id,
                Transaction.id==transaction_id 
            ) 
        )
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)
        return transaction

    def read_all(self,account_id:int):
        #find account 
        account = (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == self.user_id,
            )
            .first()
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        return self.db.scalars( #retrieve all transaction from table transaction where the account_id ==  account.id
            select(Transaction).where(Transaction.account_id == account.id)
        ).all()
       
    def update(self,account_id:int,transaction_id:int,payload:TransactionUpdate):
        account = (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == self.user_id,
            )
            .first()
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        # find the transaction
        transaction = self.db.scalar(
            select(Transaction).where(
                Transaction.account_id==account.id,
                Transaction.id==transaction_id 
            ) 
        )
    
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)
        #build update data
        update_data=payload.model_dump(exclude_unset=True)
        
        
        if update_data["amount"]:
            #changing amount
            difference=transaction.amount-update_data["amount"]        
            if transaction.transaction_type=="income":
                account.current_balance=account.current_balance - difference
                logger.info("current balance after update : %s",account.current_balance )
            if transaction.transaction_type=="expense":
                account.current_balance=account.current_balance + difference 
        
        #update
        try:
            for field,value in update_data.items():
                setattr(transaction,field,value)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Transaction updated, transaction id=%s", transaction_id)
        self.db.refresh(transaction)
        return transaction
    def delete(self,account_id:int,transaction_id:int):
        account = (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == self.user_id,
            )
            .first()
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        # find the transaction
        transaction = self.db.scalar(
            select(Transaction).where(
                Transaction.account_id==account.id,
                Transaction.id==transaction_id 
            ) 
        )
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)
        #delete
        try:
            self.db.delete(transaction)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Transaction deleted,  transaction id=%s", transaction_id) 
        return{"message":"deleted"}