#import
from fastapi import APIRouter,Depends
#schema and service and its dependency
from service.account_service import AccountService
from service.transaction_service import TransactionService
from dependencies.services import get_account_service
from dependencies.services import get_transaction_service


from datetime import datetime, timedelta, timezone
from typing import Literal

router=APIRouter(tags=["dashboard"])


#maybe make period for this month, not last 30 days
PERIODS = {
    "30d": timedelta(days=30),
    "90d": timedelta(days=90),
    "6m": timedelta(days=180),
    "1y": timedelta(days=365),
    "all": None,
}

def calculate_total(transactions, period=None):
    now = datetime.now(timezone.utc)

    if period is None:
        filtered = transactions
    else:
        start_date = now - period

        filtered = [
            t for t in transactions
            if start_date <= t.created_at <= now
        ]
    sum_expe=sum(
        t.amount for t in filtered
        if t.transaction_type == "expense"
    )
    sum_inco=sum(
        t.amount for t in filtered
        if t.transaction_type == "income"
    )
    return sum_expe,sum_inco


@router.get("/",)
def get_summary(
    accounts_serv:AccountService=Depends(get_account_service),
    transactions_serv:TransactionService=Depends(get_transaction_service),
    period: Literal["30d", "90d", "6m", "1y", "all"] = "all"

):
    accounts=accounts_serv.read_all()
    results={'period':period,
             'accounts':[]}

    duration = PERIODS[period]

    for acc in accounts:
        transactions=transactions_serv.read_all(acc.id)
        total_expenses,total_incomes = calculate_total(transactions,duration)
    
        summary={
            "account_id": acc.id,
            "total_expense":total_expenses,
            "total_income":total_incomes,
            # "account_balance":acc.current_balance,
            "last_transactions":transactions[:5]
        }
        results["accounts"].append(summary)
    return results     