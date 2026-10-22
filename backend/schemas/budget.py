from pydantic import BaseModel
from decimal import Decimal

from enum import Enum

class Period(str,Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY="monthly"

class BudgetBase(BaseModel):
    amount:Decimal
    period:Period

class BudgetUpdate(BaseModel):
    amount:Decimal  | None = None
    period:Period  | None = None

class BudgetResponse(BudgetBase):
    category_id:int