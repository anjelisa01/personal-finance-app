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
            "account_balance":acc.current_balance,
            "last_transactions":transactions[:5]
        }
        results["accounts"].append(summary)
    return results     
























'''

#function to get 
from datetime import datetime, timedelta, timezone

def calculate_expenses(transactions, period=None):
    now = datetime.now(timezone.utc)

    if period is None:
        filtered = transactions
    else:
        start_date = now - timedelta(days=period)

        filtered = [
            t for t in transactions
            if start_date <= t.created_at <= now
        ]
    return sum(
        t.amount for t in filtered
        if t.transaction_type == "expense"
    )

def calculate_total(transactions, period=None):
    now = datetime.now(timezone.utc)

    if period is None:
        filtered = transactions
    else:
        start_date = now - timedelta(days=period)

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
):
    accounts=accounts_serv.read_all()

    results=[]
    #looping dan buat calcualtion sekalian
    for acc in accounts:
        transactions=transactions_serv.read_all(acc.id)
        # sum_ex=sum(t.amount 
        #            for t in transactions 
        #            if t.transaction_type=='expense')
        # sum_in=sum(t.amount 
        #            for t in transactions 
        #            if t.transaction_type=='income')
        # summary={
        #     "account_id": acc.id,
        #     "total_expense":sum_ex,
        #     "total_income":sum_in
        # }
        # results.append(summary)


        total_expenses,total_incomes = calculate_total(transactions)
        expenses_30d,incomes_30d = calculate_total(transactions, 30)
        expenses_1y, incomes_1y= calculate_total(transactions, 365)
        summary={
            "account_id": acc.id,
            "total_expense":total_expenses,
            "total_income":total_incomes,
            "exp_30":expenses_30d,
            "inc_30":incomes_30d,
            "exp_1y":expenses_1y,
            "inc_1y":incomes_1y
        }
        results.append(summary)

    #buat t for each account
    t_per_accounts=[]
    for acc in accounts:
        t_per_accounts.append(transactions_serv.read_all(acc.id))

    results=[]
    #count expenses and income sum 
    for a in t_per_accounts:
        expenses=[]
        incomes=[]

        for t in a:
            if t.transaction_type=='expense':
                expenses.append(t)
            if t.transaction_type=='income':
                incomes.append(t)
        sum_ex=sum(x.amount for x in expenses)
        sum_in=sum(x.amount for x in incomes)
        results.append({
            'expenses': sum_ex,
            'income': sum_in,
            'balance': sum_in - sum_ex
        })
        
            


    sum_ex=sum(x.amount for x in expenses)
    sum_in=sum(x.amount for x in incomes)



    transactions=transactions_serv.read_all(accounts[0].id)


    expenses=[]
    incomes=[]

    #loop to get all expenses
    for t in transactions:
        if t.transaction_type=='expense':
            expenses.append(t)
        if t.transaction_type=='income':
            incomes.append(t)
    
    sum_ex=sum(x.amount for x in expenses)
    sum_in=sum(x.amount for x in incomes)
    

    

    return results     #accounts,transactions,expenses,incomes,sum_ex,sum_in      #accounts[0].account_name, transactions



        # amount=[]
        # for x in expenses:
        #     amount.append(x.amount)




'''