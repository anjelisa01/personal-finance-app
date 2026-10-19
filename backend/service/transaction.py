
from sqlalchemy.orm import Session

from models.transaction import Transaction
from schemas.transaction import (
    TransactionAdd,
    TransactionUpdate,
    Transfer,
)

from core.exceptions import ResourceExistedError, ResourceNotFoundError
from core.logger import logger

from repositories.transaction import TransactionRepository


class TransferService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = TransactionRepository(db)

    def create_transfer(self, tr: Transfer, payload: TransactionAdd):
        transfer_data = tr.model_dump(exclude_unset=True)
        account_in = transfer_data['account_id_in']
        account_out = transfer_data['account_id_out']

        transaction = Transaction(**payload.model_dump())
        transaction.account_id = transfer_data['account_id_in']
        transaction.transaction_type = 'transfer'
        transaction.transfer_direction = 'outgoing'

        if transaction.category_id == 0:
            transaction.category_id = None

        try:
            transaction = self.repository.create(transaction)
        except Exception:
            self.db.rollback()
            raise

        logger.info(
            "Transaction created, transaction id=%s",
            transaction.id,
        )
        return transaction

        '''
        generate transfer_id
        transaction_type="transfer"
        add_transaction(account_id_in,transfer_id,transfer_direction='incoming',transaction_type)
        add_transaction(account_id_out,transfer_id,transfer_direction='outgoing',transaction_type)
        '''


class TransactionService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = TransactionRepository(db)

    def create_transfer(
        self,
        account_out: int,
        account_in: int,
        payload: TransactionAdd,
    ):
        out_transaction = Transaction(**payload.model_dump())
        out_transaction.account_id = account_out
        out_transaction.transaction_type = 'transfer'
        out_transaction.transfer_id = (
            self.repository.get_next_transfer_id()
        )
        out_transaction.transfer_direction = 'outgoing'

        in_transaction = Transaction(**payload.model_dump())
        in_transaction.account_id = account_in
        in_transaction.transaction_type = 'transfer'
        in_transaction.transfer_id = out_transaction.transfer_id
        in_transaction.transfer_direction = 'incoming'

        if out_transaction.category_id == 0:
            out_transaction.category_id = None
            in_transaction.category_id = None

        try:
            self.repository.create_all(
                [out_transaction, in_transaction]
            )
        except Exception:
            self.db.rollback()
            raise

        return self.repository.get_by_transfer_id(
            out_transaction.transfer_id
        )

    def create(self, account_id: int, payload: TransactionAdd):
        account = self.repository.get_account(
            account_id, self.user_id
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        transaction = Transaction(**payload.model_dump())
        transaction.account_id = account.id

        # update account balance
        # if transaction.transaction_type=="expense":
        #     account.current_balance=account.current_balance - transaction.amount
        # if transaction.transaction_type=="income":
        #     account.current_balance=account.current_balance + transaction.amount

        if transaction.category_id == 0:
            transaction.category_id = None

        try:
            transaction = self.repository.create(transaction)
        except Exception:
            self.db.rollback()
            raise

        logger.info(
            "Transaction created, transaction id=%s",
            transaction.id,
        )
        return transaction

    def read_one(self, account_id: int, transaction_id: int):
        account = self.repository.get_account(
            account_id, self.user_id
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        transaction = self.repository.get_by_id(
            account.id, transaction_id
        )
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)

        return transaction

    def read_all(self, account_id: int):
        account = self.repository.get_account(
            account_id, self.user_id
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        return self.repository.get_all(account.id)

    def update(
        self,
        account_id: int,
        transaction_id: int,
        payload: TransactionUpdate,
    ):
        account = self.repository.get_account(
            account_id, self.user_id
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        transaction = self.repository.get_by_id(
            account.id, transaction_id
        )
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)

        update_data = payload.model_dump(exclude_unset=True)

        if update_data["amount"]:
            difference = transaction.amount - update_data["amount"]

            if transaction.transaction_type == "income":
                account.current_balance = (
                    account.current_balance - difference
                )
                logger.info(
                    "current balance after update : %s",
                    account.current_balance,
                )

            if transaction.transaction_type == "expense":
                account.current_balance = (
                    account.current_balance + difference
                )

        try:
            transaction = self.repository.update(
                transaction, update_data
            )
        except Exception:
            self.db.rollback()
            raise

        logger.info(
            "Transaction updated, transaction id=%s",
            transaction_id,
        )
        return transaction

    def delete(self, account_id: int, transaction_id: int):
        account = self.repository.get_account(
            account_id, self.user_id
        )
        if account is None:
            raise ResourceNotFoundError("Account", account_id)

        transaction = self.repository.get_by_id(
            account.id, transaction_id
        )
        if transaction is None:
            raise ResourceNotFoundError("Transaction", transaction_id)

        try:
            self.repository.delete(transaction)
        except Exception:
            self.db.rollback()
            raise

        logger.info(
            "Transaction deleted, transaction id=%s",
            transaction_id,
        )
        return {"message": "deleted"}
