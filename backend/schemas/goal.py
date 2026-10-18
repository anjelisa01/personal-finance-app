from pydantic import BaseModel,ConfigDict
from datetime import datetime,date
from decimal import Decimal
class GoalBase(BaseModel):
    goal_name:str
    target_amount:Decimal
    due_date:date
    account_id:int | None=None
    model_config = ConfigDict(from_attributes=True)
class GoalResponse(GoalBase):
    id:int

class GoalUpdate(BaseModel):
    goal_name:str | None = None 
    target_amount:float | None = None 
    saved_amount:float | None = None 
    due_date:datetime | None = None 
    account_id:int | None=None
    model_config = ConfigDict(from_attributes=True)