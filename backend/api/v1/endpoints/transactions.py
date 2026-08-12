from fastapi import APIRouter,Depends
#pydantic schemas
from schemas.transaction import TransactionAdd,TransactionResponse,TransactionUpdate

# services
from service.transaction_service import TransactionService

#dependencies
from dependencies.services import get_transaction_service

router=APIRouter(tags=["transactions"])

#Add new transaction
@router.post("/",response_model=TransactionResponse)
def add_transaction(
    account_id:int,
    payload:TransactionAdd,
    service:TransactionService=Depends(get_transaction_service)):
    return service.create(account_id,payload)

#Get all transactions 
@router.get("/",response_model=list[TransactionResponse])   
def get_all_transaction(
    account_id:int,
    service:TransactionService=Depends(get_transaction_service)):
    return service.read_all(account_id)

#Get one transaction
@router.get("/{transaction_id}",response_model=TransactionResponse)
def get_one_transaction(
    account_id:int,
    transaction_id:int,
    service:TransactionService=Depends(get_transaction_service)):  
    return service.read_one(account_id,transaction_id)
 
# #Update transaction
@router.patch("/{transaction_id}",response_model=TransactionResponse)
def edit_transaction(
    account_id:int,
    transaction_id:int,
    payload:TransactionUpdate,
    service:TransactionService=Depends(get_transaction_service)):
    return service.update(account_id,transaction_id,payload)

# #delete transaction
@router.delete("/{transaction_id}")  
def remove_transaction(
    account_id:int,
    transaction_id:int,
    service:TransactionService=Depends(get_transaction_service)):
    return service.delete(account_id,transaction_id)

