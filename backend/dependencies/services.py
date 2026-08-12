from fastapi import Depends

from service.user_service import UserService
from service.goal_service import GoalService
from service.account_service import AccountService
from service.auth_service import AuthService
from service.budget_service import BudgetService
from service.category_service import CategoryService
from service.transaction_service import TransactionService

from dependencies.auth import get_current_user
from dependencies.database import get_db

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

def get_goal_service(db: Session = Depends(get_db),user_id:int=Depends(get_current_user)):
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