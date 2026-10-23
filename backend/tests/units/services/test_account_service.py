from unittest.mock import MagicMock
from types import SimpleNamespace

import pytest

from services.account import AccountService
from schemas.account import AccountBase, AccountUpdate
from core.exceptions import ResourceExistedError, ResourceNotFoundError

def make_service():
    db = MagicMock()
    service = AccountService(db, user_id=1)
    service.repository = MagicMock()
    return service, db


def test_create_account():
    service, _ = make_service()
    service.repository.get_by_name.return_value = None

    saved_account = SimpleNamespace(
        id=10,
        account_name="Bni debit",
        user_id=1,
    )
    service.repository.create.return_value = saved_account

    payload = AccountBase(
        account_name="Bni debit",
        initial_balance=40000,
    )

    result = service.create(payload)

    assert result == saved_account

    created = service.repository.create.call_args.args[0]
    assert created.account_name == "Bni debit"
    assert created.user_id == 1


def test_create_duplicate_account():
    service, _ = make_service()
    service.repository.get_by_name.return_value = MagicMock()

    payload = AccountBase(
        account_name="Bni debit",
        initial_balance=40000,
    )

    with pytest.raises(ResourceExistedError):
        service.create(payload)

    service.repository.create.assert_not_called()


def test_read_one_account_not_found():
    service, _ = make_service()
    service.repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.read_one(account_id=10)


def test_read_all_accounts():
    service, _ = make_service()
    accounts = [MagicMock(), MagicMock()]
    service.repository.get_all.return_value = accounts

    result = service.read_all()

    assert result == accounts
    service.repository.get_all.assert_called_once_with(1)


def test_update_account():
    service, _ = make_service()
    account = SimpleNamespace(id=10, account_name="Bni debit")
    service.repository.get_by_id.return_value = account
    service.repository.update.return_value = account

    payload = AccountUpdate(initial_balance=50000)

    result = service.update(account_id=10, payload=payload)

    assert result == account

    service.repository.update.assert_called_once_with(
        account,
        {"initial_balance": 50000},
    )


def test_update_duplicate_account_name():
    service, _ = make_service()

    account = SimpleNamespace(id=10, account_name="Bni debit")
    another_account = SimpleNamespace(id=20, account_name="Bni credit")

    service.repository.get_by_id.return_value = account
    service.repository.get_by_name.return_value = another_account

    payload = AccountUpdate(account_name="Bni credit")

    with pytest.raises(ResourceExistedError):
        service.update(account_id=10, payload=payload)

    service.repository.update.assert_not_called()


def test_delete_account():
    service, _ = make_service()
    account = SimpleNamespace(id=10)
    service.repository.get_by_id.return_value = account

    result = service.delete(account_id=10)

    assert result == {"message": "deleted"}
    service.repository.delete.assert_called_once_with(account)


def test_create_account_rolls_back_on_error():
    service, db = make_service()
    service.repository.get_by_name.return_value = None
    service.repository.create.side_effect = RuntimeError("Database error")

    payload = AccountBase(
        account_name="Bni debit",
        initial_balance=40000,
    )

    with pytest.raises(RuntimeError):
        service.create(payload)

    db.rollback.assert_called_once()