from pydantic import EmailStr,BaseModel,ConfigDict

#base
class UserBase(BaseModel):
    name:str
    email:EmailStr
    currency:str 

#Input user
class UserCreate(UserBase):
    password:str
class UserUpdate(BaseModel):
    name:str | None = None 
    email:str | None = None
    password:str | None=None
    currency:str | None=None
    model_config = ConfigDict(from_attributes=True)

#output system
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)