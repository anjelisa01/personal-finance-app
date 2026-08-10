from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import UserLogin                                                      
from service.auth_service import AuthService
from dependencies.services import get_auth_service

router=APIRouter(tags=["auth"])

@router.post("/login") #i changed from userlogin to authformbearer
def auth_login(form_data: OAuth2PasswordRequestForm = Depends(),service:AuthService=Depends(get_auth_service)):      #(form:UserLogin,service:AuthService=Depends(get_auth_service)):
    payload = UserLogin(
        email=form_data.username,  # Swagger username = your email
        password=form_data.password
    )
    return service.login(payload)