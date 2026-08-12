from pydantic import BaseModel

class BudgetBase(BaseModel):
    limit:float
    period:str

class BudgetUpdate(BaseModel):
    limit:float  | None = None
    period:str  | None = None