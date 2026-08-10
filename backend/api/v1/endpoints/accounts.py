#import
from fastapi import APIRouter,Depends

#schema and service and its dependency
from schemas.account import AccountBase,AccountResponse,AccountUpdate
from service.account_service import AccountService
from dependencies.services import get_account_service

router=APIRouter(tags=["accounts"])

@router.post("/",response_model=AccountResponse)
def add_account(
    payload:AccountBase,
    service:AccountService=Depends(get_account_service)):
    return service.create(payload)

@router.get("/",response_model=list[AccountResponse])   
def get_all_accounts(
    service:AccountService=Depends(get_account_service)):
    return service.read_all()

@router.get("/{account_id}",response_model=AccountResponse)
def get_one_accounts(
    account_id:int,
    service:AccountService=Depends(get_account_service)):  
    return service.read_one(account_id)

@router.patch("/{account_id}",response_model=AccountResponse)
def edit_account(
    account_id:int,
    payload:AccountUpdate,
    service:AccountService=Depends(get_account_service)):
    return service.update(account_id,payload)

@router.delete("/{account_id}")  
def remove_account(
    account_id:int,
    service:AccountService=Depends(get_account_service)):
    return service.delete(account_id)