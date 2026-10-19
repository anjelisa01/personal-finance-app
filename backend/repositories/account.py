
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.account import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, user_id: int, account_name: str):
        stmt = select(Account).where(
            Account.user_id == user_id,
            Account.account_name == account_name,
        )
        return self.db.scalars(stmt).first()

    def get_by_id(self, user_id: int, account_id: int):
        stmt = select(Account).where(
            Account.user_id == user_id,
            Account.id == account_id,
        )
        return self.db.scalar(stmt)

    def get_all(self, user_id: int):
        stmt = select(Account).where(
            Account.user_id == user_id
        )
        return self.db.scalars(stmt).all()

    def create(self, account: Account):
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account: Account, update_data: dict):
        for field, value in update_data.items():
            setattr(account, field, value)

        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account: Account):
        self.db.delete(account)
        self.db.commit()
