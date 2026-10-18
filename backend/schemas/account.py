from pydantic import BaseModel
from decimal import Decimal

class AccountBase(BaseModel):
    account_name:str
    initial_balance:Decimal
class AccountUpdate(BaseModel):
    initial_balance:float  | None = None
    account_name:str  | None = None
class AccountResponse(AccountBase):
    id:int
    