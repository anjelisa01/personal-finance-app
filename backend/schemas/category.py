from pydantic import BaseModel
from enum import Enum
from sqlalchemy import Enum as SQLEnum
class CategoryType(str,Enum):
    EXPENSE = "expense"
    INCOME = "income"

class CategoryBase(BaseModel):
    category_name:str 
    category_type:CategoryType

class CategoryUpdate(BaseModel):
    category_name:str  | None = None
    category_type:CategoryType | None = None

class CategoryResponse(CategoryBase):
    id:int
