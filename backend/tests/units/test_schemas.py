import pytest
from pydantic import ValidationError
from decimal import Decimal
from datetime import date

from schemas.account import AccountBase, AccountUpdate,AccountResponse
from schemas.auth import UserLogin
from schemas.budget import BudgetBase, BudgetUpdate, Period
from schemas.category import CategoryBase, CategoryResponse,CategoryType
from schemas.dashboard import DashboardSummary
from schemas.goal import GoalBase, GoalResponse, GoalUpdate
from schemas.transaction import TransactionAdd, TransactionUpdate, TransactionResponse, Transfer,TransactionType, Direction
from schemas.user import UserCreate, UserUpdate, UserResponse

#=============================================account
def test_create_account():
    account = AccountBase(
        account_name="Bni debit",
        initial_balance=40000
    )
    assert account.account_name == "Bni debit"
    assert account.initial_balance == 40000
def test_create_account_missing_field():
    with pytest.raises(ValidationError):
        AccountBase(account_name="Bni debit")
def test_update_account_partial():
    account = AccountUpdate(account_name="Bni credit")
    assert account.account_name == "Bni credit"
    assert account.initial_balance is None
def test_update_account_empty():
    account = AccountUpdate()
    assert account.account_name is None
    assert account.initial_balance is None
def test_account_response():
    account = AccountResponse(
        id=1,
        account_name="Bni debit",
        initial_balance=40000
    )
    assert account.id == 1
    assert account.account_name == "Bni debit"
    assert account.initial_balance == 40000
#============================================user
def test_user_create_missing_password():
    with pytest.raises(ValidationError):
        UserCreate(
            name="Alice",
            email="alice@example.com",
            currency="IDR",
        )
def test_user_update_empty():
    user = UserUpdate()
    assert user.name is None
    assert user.email is None
def test_user_response():
    user = UserResponse(
        name="Alice",
        email="alice@example.com",
        currency="IDR",
    )
    assert user.name == "Alice"
#=============================================budget
def test_budget_valid():
    budget = BudgetBase(amount=Decimal("500000"), period="monthly")
    assert budget.period == Period.MONTHLY
def test_budget_invalid_period():
    with pytest.raises(ValidationError):
        BudgetBase(amount=500000, period="yearly")
def test_budget_update_partial():
    budget = BudgetUpdate(amount=100000)
    assert budget.amount == Decimal("100000")
    assert budget.period is None
#=============================================goal
def test_goal_valid():
    goal = GoalBase(
        goal_name="New laptop",
        target_amount=Decimal("10000000"),
        due_date=date(2027, 6, 1),
    )
    assert goal.goal_name == "New laptop"
    assert goal.account_id is None
def test_goal_response():
    goal = GoalResponse(
        id=1,
        goal_name="New laptop",
        target_amount=Decimal("10000000"),
        due_date=date(2027, 6, 1),
    )
    assert goal.id == 1
def test_goal_update_empty():
    goal = GoalUpdate()
    assert goal.goal_name is None
    assert goal.target_amount is None
#=============================================transaction
def test_transaction_add_valid():
    transaction = TransactionAdd(
        title="Lunch",
        amount=Decimal("50000"),
        note="Lunch expense",
        transaction_type="expense",
    )
    assert transaction.transaction_type == TransactionType.EXPENSE
    assert transaction.category_id is None
def test_transaction_add_missing_required_field():
    with pytest.raises(ValidationError):
        TransactionAdd(
            title="Lunch",
            amount=Decimal("50000"),
            transaction_type="expense",
        )
def test_transaction_update_partial():
    transaction = TransactionUpdate(title="Dinner")
    assert transaction.title == "Dinner"
    assert transaction.amount is None
def test_transaction_response():
    transaction = TransactionResponse(
        id=1,
        account_id=2,
        title="Lunch",
        amount=Decimal("50000"),
        note="Lunch expense",
        transaction_type="expense",
    )
    assert transaction.id == 1
    assert transaction.account_id == 2
#---------------------------------------------transaction=transfer
def test_transfer_valid():
    transfer = Transfer(account_id_in=2, account_id_out=1)
    assert transfer.account_id_in == 2
    assert transfer.account_id_out == 1
def test_transfer_missing_account():
    with pytest.raises(ValidationError):
        Transfer(account_id_in=2)
#=============================================category
def test_category_valid():
    category = CategoryBase(
        category_name="Food",
        category_type="expense",
    )
    assert category.category_type == CategoryType.EXPENSE
def test_category_response():
    category = CategoryResponse(
        id=1,
        category_name="Salary",
        category_type="income",
    )
    assert category.id == 1
#=============================================dashboard
def test_dashboard_summary():
    summary = DashboardSummary(expenses=Decimal("250000"))
    assert summary.expenses == Decimal("250000")
#=============================================auth
def test_user_login_valid():
    user = UserLogin(email="alice@example.com", password="123")
    assert user.email == "alice@example.com"
def test_user_login_invalid_email():
    with pytest.raises(ValidationError):
        UserLogin(email="invalid-email", password="123")
#=============================================