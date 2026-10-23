from fastapi import Depends
from sqlalchemy.orm import Session

from services.user import UserService
from services.goal import GoalService
from services.account import AccountService
from services.auth import AuthService
from services.budget import BudgetService
from services.category import CategoryService
from services.transaction import TransactionService

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