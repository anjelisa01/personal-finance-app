from pydantic import BaseModel, Field, EmailStr

#----------input from  user----------
class UserLogin(BaseModel):
    email:EmailStr
    password:str=Field(...,min_length=2)