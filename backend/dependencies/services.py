from fastapi import Depends

from service.user import UserService
from service.goal import GoalService
from service.account import AccountService
from service.auth import AuthService
from service.budget import BudgetService
from service.category import CategoryService
from service.transaction import TransactionService

from dependencies.auth import get_current_user
from dependencies.database import get_db

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

def get_goal_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
    print("GOAL SERVICE user_id:", repr(user_id))
    return GoalService(db,user_id)

def get_account_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
    return AccountService(db,user_id)

def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

def get_category_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
    return CategoryService(db,user_id)

def get_budget_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
    return BudgetService(db,user_id)

def get_transaction_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
    return TransactionService(db,user_id)