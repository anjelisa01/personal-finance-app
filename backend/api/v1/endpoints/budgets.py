from fastapi import APIRouter,Depends
from schemas.budget import BudgetBase,BudgetUpdate

# services
from service.budget_service import BudgetService
#dependencies
from dependencies.services import get_budget_service

router=APIRouter(tags=["budgets"])

@router.post("/",response_model=BudgetBase)
def add_budget(
    category_id:int,
    payload:BudgetBase,
    service:BudgetService=Depends(get_budget_service)):
    return service.create(category_id,payload)

@router.get("/",response_model=BudgetBase)
def get_one_budget(
    category_id:int,
    service:BudgetService=Depends(get_budget_service)):
    return service.read_one(category_id)

@router.patch("/",response_model=BudgetBase)
def edit_budget(
    category_id:int,
    payload:BudgetUpdate,
    service:BudgetService=Depends(get_budget_service)):
    return service.update(category_id,payload)

@router.delete("/")
def remove_budget(
    category_id:int,
    service:BudgetService=Depends(get_budget_service)):
    return service.delete(category_id)