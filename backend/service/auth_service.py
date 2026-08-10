#import
from sqlalchemy.orm import Session

from schemas.auth import UserLogin

from core.security import get_user_by_email,verify_password,create_access_token
from core.logger import logger
from core.exceptions import AuthFailedCredential

class AuthService:
    def __init__(self,db: Session):
        self.db = db
    def login(self,payload:UserLogin):
        existed_user=get_user_by_email(self.db,payload.email)
        if not existed_user or not verify_password(self.db,payload.password,existed_user.hashed_password):
            raise AuthFailedCredential()

        try:
            token=create_access_token({"user_id":str(existed_user.id)})
        except Exception:
            raise

        logger.info("User created token. user_id=%s", existed_user.id)
        return {"access_token":token,"token-type":"bearer"}