from fastapi import APIRouter
from api.v1.endpoints import auth,users,transactions,accounts,categories,goals,budgets,dashboard

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    transactions.router,
    prefix="/accounts/{account_id}/transactions",
    tags=["transactions"]
)

api_router.include_router(
    accounts.router,
    prefix="/accounts",
    tags=["accounts"]
)

api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["categories"]
)
api_router.include_router(
    goals.router,
    prefix="/goals",
    tags=["goals"]
)

api_router.include_router(
    budgets.router,
    prefix="/categories/{category_id}/budget",
    tags=["budgets"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"]
)