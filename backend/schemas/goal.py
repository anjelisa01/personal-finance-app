from pydantic import BaseModel,ConfigDict
from datetime import datetime

class GoalBase(BaseModel):
    goal_name:str
    target_amount:float
    saved_amount:float
    due_date:datetime
    model_config = ConfigDict(from_attributes=True)
class GoalResponse(GoalBase):
    id:int

class GoalUpdate(BaseModel):
    goal_name:str | None = None 
    target_amount:float | None = None 
    saved_amount:float | None = None 
    due_date:datetime | None = None 
    model_config = ConfigDict(from_attributes=True)