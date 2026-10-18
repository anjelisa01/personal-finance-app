from pydantic import BaseModel,ConfigDict,Field
from enum import Enum
from decimal import Decimal


class TransactionType(str,Enum):
    EXPENSE = "expense"
    INCOME = "income"
    SAVING="transfer"
class Direction(str,Enum):
    INCOMING="incoming"
    OUTGOING="outgoing"

#Input user
class TransactionAdd(BaseModel):
    title:str
    amount:Decimal
    note:str
    category_id:int | None = None #make default=None
    transaction_type:TransactionType
    transfer_id:int | None = None
    transfer_direction:Direction | None = Field(
        default=None,
        json_schema_extra={"example": None},
    )

class Transfer(BaseModel):
    account_id_in:int
    account_id_out:int

    '''
    generate transfer_id
    transaction_type="transfer"
    add_transaction(account_id_in,transfer_direction='incoming',transaction_type)
    add_transaction(account_id_out,transfer_direction='outgoing',transaction_type)
    '''   

class TransactionUpdate(BaseModel):
    title:str | None = None 
    amount:Decimal | None = None
    note:str | None=None
    category_id:int|None=None
    transaction_type: TransactionType | None=None
    transfer_id:int | None = None
    transfer_direction:Direction | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
#output system
class TransactionResponse(TransactionAdd):
    id:int
    account_id:int
    model_config = ConfigDict(from_attributes=True)