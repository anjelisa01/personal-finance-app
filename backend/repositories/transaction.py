
from sqlalchemy.orm import Session
from sqlalchemy import select, text

from models.transaction import Transaction
from models.account import Account


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_account(self, account_id: int, user_id: int):
        return (
            self.db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == user_id,
            )
            .first()
        )

    def get_by_id(self, account_id: int, transaction_id: int):
        return self.db.scalar(
            select(Transaction).where(
                Transaction.account_id == account_id,
                Transaction.id == transaction_id,
            )
        )

    def get_all(self, account_id: int):
        return self.db.scalars(
            select(Transaction).where(
                Transaction.account_id == account_id
            )
        ).all()

    def get_next_transfer_id(self):
        return self.db.execute(
            text("SELECT nextval('transfer_id_seq')")
        ).scalar_one()

    def get_by_transfer_id(self, transfer_id: int):
        return self.db.scalars(
            select(Transaction).where(
                Transaction.transfer_id == transfer_id
            )
        ).all()

    def create(self, transaction: Transaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def create_all(self, transactions: list[Transaction]):
        self.db.add_all(transactions)
        self.db.commit()

    def update(self, transaction: Transaction, update_data: dict):
        for field, value in update_data.items():
            setattr(transaction, field, value)

        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction):
        self.db.delete(transaction)
        self.db.commit()
