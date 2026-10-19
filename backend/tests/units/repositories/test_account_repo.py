#==================================ACCOUNT 
from unittest.mock import MagicMock
from types import SimpleNamespace
from sqlalchemy.orm import Session

from repositories.account import AccountRepository


def make_repo():
    db = MagicMock(spec=Session)
    repo = AccountRepository(db)
    return repo, db


def test_get_by_name():
    repo, db = make_repo()
    account = SimpleNamespace(account_name="Bni debit")

    db.scalars.return_value.first.return_value = account

    result = repo.get_by_name(1, "Bni debit")

    assert result == account
    db.scalars.return_value.first.assert_called_once()


def test_get_by_id():
    repo, db = make_repo()
    account = SimpleNamespace(id=1)

    db.scalar.return_value = account

    result = repo.get_by_id(1, 1)

    assert result == account
    db.scalar.assert_called_once()


def test_get_all():
    repo, db = make_repo()
    accounts = [
        SimpleNamespace(id=1),
        SimpleNamespace(id=2),
    ]

    db.scalars.return_value.all.return_value = accounts

    result = repo.get_all(1)

    assert result == accounts
    assert len(result) == 2


def test_create():
    repo, db = make_repo()
    account = SimpleNamespace(account_name="Bni debit")

    result = repo.create(account)

    assert result == account
    db.add.assert_called_once_with(account)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(account)


def test_update():
    repo, db = make_repo()
    account = SimpleNamespace(account_name="Bni debit")

    result = repo.update(
        account,
        {"account_name": "Bni credit"},
    )

    assert result.account_name == "Bni credit"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(account)


def test_delete():
    repo, db = make_repo()
    account = SimpleNamespace(id=1)

    result = repo.delete(account)

    assert result is None
    db.delete.assert_called_once_with(account)
    db.commit.assert_called_once()
    