from pydantic import BaseModel,ConfigDict
from enum import Enum
from decimal import Decimal

class TransactionType(str,Enum):
    EXPENSE = "expense"
    INCOME = "income"
    SAVING="transfer"

#Input user
class TransactionAdd(BaseModel):
    title:str
    amount:Decimal
    note:str
    category_id:int | None = None #make default=None
    transaction_type:TransactionType
    
class TransactionUpdate(BaseModel):
    title:str | None = None 
    amount:Decimal | None = None
    note:str | None=None
    category_id:int|None=None
    transaction_type: TransactionType | None=None
    model_config = ConfigDict(from_attributes=True)
    
#output system
class TransactionResponse(TransactionAdd):
    id:int
    account_id:int
    model_config = ConfigDict(from_attributes=True)