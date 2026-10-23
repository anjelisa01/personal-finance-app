
from sqlalchemy.orm import Session

from models.account import Account
from schemas.account import AccountBase, AccountUpdate
from repositories.account import AccountRepository

from core.logger import logger
from core.exceptions import ResourceExistedError, ResourceNotFoundError


class AccountService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = AccountRepository(db)

    def create(self, payload: AccountBase):
        existing = self.repository.get_by_name(
            self.user_id, payload.account_name
        )
        if existing:
            raise ResourceExistedError("Account", payload.account_name)

        account = Account(**payload.model_dump())
        account.user_id = self.user_id

        try:
            account = self.repository.create(account)
        except Exception:
            self.db.rollback()
            raise

        logger.info("New Account created, account id=%s", account.id)
        return account

    def read_one(self, account_id: int):
        account = self.repository.get_by_id(self.user_id, account_id)
        if account is None:
            raise ResourceNotFoundError("Account", account_id)
        return account

    def read_all(self):
        return self.repository.get_all(self.user_id)

    def update(self, account_id: int, payload: AccountUpdate):
        account = self.read_one(account_id)
        update_data = payload.model_dump(exclude_unset=True)

        if "account_name" in update_data:
            existing = self.repository.get_by_name(
                self.user_id, update_data["account_name"]
            )
            if existing and existing.id != account_id:
                raise ResourceExistedError(
                    "Account", update_data["account_name"]
                )

        try:
            account = self.repository.update(account, update_data)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Account updated, account id=%s", account_id)
        return account

    def delete(self, account_id: int):
        account = self.read_one(account_id)

        try:
            self.repository.delete(account)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Account deleted, account id=%s", account_id)
        return {"message": "deleted"}
