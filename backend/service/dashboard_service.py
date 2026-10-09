#service for dashboard endpoint

#import
from sqlalchemy.orm import Session
from sqlalchemy import select

#utils
from core.logger import logger
from core.exceptions import ResourceExistedError,ResourceNotFoundError

#i need, table transaction, user, and account
from models.user import User
from models.transaction import Transaction
from models.account import Account

#i need read_all transactions, and read_all accounts
from service.account_service import AccountService
from service.transaction_service import TransactionService

#schema i need is a response schema:
from schemas.dashboard import DashboardSummary

from fastapi import Depends
from dependencies.services import get_account_service


class DashboardService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id
    def get_summary(self,service:AccountService=Depends(get_account_service)):
        '''
        i want to view:
        sum of each transactions by all accounts.

        so:
        user id
        every accounts belong to user id
        sum of expenses and incomes of each account
        '''

        #first, return list of accounts
        service.read_all()




        