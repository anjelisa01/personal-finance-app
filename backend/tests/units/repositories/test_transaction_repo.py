
#==================================TRANSACTION
from unittest.mock import MagicMock
from types import SimpleNamespace
from sqlalchemy.orm import Session

from models.account import Account
from repositories.transaction import TransactionRepository


def make_repo():
    db = MagicMock(spec=Session)
    return TransactionRepository(db), db


def test_get_account():
    repo, db = make_repo()
    account = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = account

    result = repo.get_account(account_id=1, user_id=2)

    assert result == account
    db.query.assert_called_once_with(Account)


def test_get_by_id():
    repo, db = make_repo()
    transaction = MagicMock()

    db.scalar.return_value = transaction

    result = repo.get_by_id(account_id=1, transaction_id=10)

    assert result == transaction
    db.scalar.assert_called_once()


def test_get_all():
    repo, db = make_repo()
    transactions = [MagicMock(), MagicMock()]

    db.scalars.return_value.all.return_value = transactions

    result = repo.get_all(account_id=1)

    assert result == transactions
    assert len(result) == 2


def test_get_next_transfer_id():
    repo, db = make_repo()

    db.execute.return_value.scalar_one.return_value = 100

    result = repo.get_next_transfer_id()

    assert result == 100
    db.execute.assert_called_once()


def test_get_by_transfer_id():
    repo, db = make_repo()
    transactions = [MagicMock(), MagicMock()]

    db.scalars.return_value.all.return_value = transactions

    result = repo.get_by_transfer_id(transfer_id=100)

    assert result == transactions
    db.scalars.assert_called_once()


def test_create_transaction():
    repo, db = make_repo()
    transaction = MagicMock()

    result = repo.create(transaction)

    assert result == transaction
    db.add.assert_called_once_with(transaction)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(transaction)


def test_create_all_transactions():
    repo, db = make_repo()
    transactions = [MagicMock(), MagicMock()]

    result = repo.create_all(transactions)

    assert result is None
    db.add_all.assert_called_once_with(transactions)
    db.commit.assert_called_once()


def test_update_transaction():
    repo, db = make_repo()
    transaction = SimpleNamespace(title="Lunch", amount=10000)

    result = repo.update(transaction, {"title": "Dinner"})

    assert result.title == "Dinner"
    assert result.amount == 10000
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(transaction)


def test_delete_transaction():
    repo, db = make_repo()
    transaction = MagicMock()

    result = repo.delete(transaction)

    assert result is None
    db.delete.assert_called_once_with(transaction)
    db.commit.assert_called_once()
