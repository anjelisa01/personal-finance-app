
# tests/unit/test_transaction_service.py

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from services.transaction import TransactionService, TransferService
from core.exceptions import ResourceNotFoundError


@pytest.fixture
def service():
    db = MagicMock()
    service = TransactionService(db, user_id=1)
    service.repository = MagicMock()
    return service


@pytest.fixture
def payload():
    data = MagicMock()
    data.model_dump.return_value = {
        "amount": 100,
        "category_id": 0,
        "transaction_type": "expense",
    }
    return data


def test_create_transaction(service, payload):
    account = SimpleNamespace(id=10)
    service.repository.get_account.return_value = account
    service.repository.create.side_effect = lambda transaction: transaction

    result = service.create(10, payload)

    assert result.account_id == 10
    assert result.category_id is None
    service.repository.create.assert_called_once()


def test_create_transaction_account_not_found(service, payload):
    service.repository.get_account.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.create(10, payload)

    service.repository.create.assert_not_called()


def test_create_transaction_rolls_back_on_error(service, payload):
    service.repository.get_account.return_value = SimpleNamespace(id=10)
    service.repository.create.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.create(10, payload)

    service.db.rollback.assert_called_once()


def test_read_one_transaction(service):
    account = SimpleNamespace(id=10)
    transaction = SimpleNamespace(id=20)

    service.repository.get_account.return_value = account
    service.repository.get_by_id.return_value = transaction

    result = service.read_one(10, 20)

    assert result == transaction
    service.repository.get_by_id.assert_called_once_with(10, 20)


def test_read_one_transaction_not_found(service):
    service.repository.get_account.return_value = SimpleNamespace(id=10)
    service.repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.read_one(10, 20)


def test_read_all_transactions(service):
    account = SimpleNamespace(id=10)
    transactions = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    service.repository.get_account.return_value = account
    service.repository.get_all.return_value = transactions

    result = service.read_all(10)

    assert result == transactions
    service.repository.get_all.assert_called_once_with(10)


def test_update_transaction(service, payload):
    account = SimpleNamespace(id=10, current_balance=500)
    transaction = SimpleNamespace(
        id=20,
        amount=100,
        transaction_type="expense",
    )
    updated_transaction = SimpleNamespace(id=20, amount=150)

    payload.model_dump.return_value = {"amount": 150}
    service.repository.get_account.return_value = account
    service.repository.get_by_id.return_value = transaction
    service.repository.update.return_value = updated_transaction

    result = service.update(10, 20, payload)

    assert result == updated_transaction
    service.repository.update.assert_called_once_with(
        transaction, {"amount": 150}
    )


def test_delete_transaction(service):
    account = SimpleNamespace(id=10)
    transaction = SimpleNamespace(id=20)

    service.repository.get_account.return_value = account
    service.repository.get_by_id.return_value = transaction

    result = service.delete(10, 20)

    assert result == {"message": "deleted"}
    service.repository.delete.assert_called_once_with(transaction)


def test_create_transfer(service, payload):
    payload.model_dump.return_value = {
        "amount": 100,
        "category_id": 0,
        "transaction_type": "expense",
    }
    service.repository.get_next_transfer_id.return_value = 5
    expected = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    service.repository.get_by_transfer_id.return_value = expected

    result = service.create_transfer(10, 20, payload)

    service.repository.create_all.assert_called_once()
    transactions = service.repository.create_all.call_args.args[0]

    assert len(transactions) == 2
    assert transactions[0].account_id == 10
    assert transactions[1].account_id == 20
    assert transactions[0].transfer_id == 5
    assert transactions[1].transfer_id == 5
    assert transactions[0].transfer_direction == "outgoing"
    assert transactions[1].transfer_direction == "incoming"
    assert transactions[0].category_id is None
    assert transactions[1].category_id is None
    assert result == expected


def test_create_transfer_rolls_back_on_error(service, payload):
    service.repository.get_next_transfer_id.return_value = 5
    service.repository.create_all.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.create_transfer(10, 20, payload)

    service.db.rollback.assert_called_once()


def test_update_transaction_rolls_back_on_error(service, payload):
    account = SimpleNamespace(id=10, current_balance=500)
    transaction = SimpleNamespace(
        id=20,
        amount=100,
        transaction_type="expense",
    )

    payload.model_dump.return_value = {"amount": 150}
    service.repository.get_account.return_value = account
    service.repository.get_by_id.return_value = transaction
    service.repository.update.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.update(10, 20, payload)

    service.db.rollback.assert_called_once()


# TransferService tests

@pytest.fixture
def transfer_service():
    db = MagicMock()
    service = TransferService(db, user_id=1)
    service.repository = MagicMock()
    return service


def test_transfer_service_create_transfer(transfer_service, payload):
    transfer = MagicMock()
    transfer.model_dump.return_value = {
        "account_id_in": 20,
        "account_id_out": 10,
    }
    payload.model_dump.return_value = {
        "amount": 100,
        "category_id": 0,
        "transaction_type": "expense",
    }
    transfer_service.repository.create.side_effect = lambda transaction: transaction

    result = transfer_service.create_transfer(transfer, payload)

    assert result.account_id == 20
    assert result.transaction_type == "transfer"
    assert result.transfer_direction == "outgoing"
    assert result.category_id is None


def test_transfer_service_rolls_back_on_error(
    transfer_service, payload
):
    transfer = MagicMock()
    transfer.model_dump.return_value = {
        "account_id_in": 20,
        "account_id_out": 10,
    }
    transfer_service.repository.create.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        transfer_service.create_transfer(transfer, payload)

    transfer_service.db.rollback.assert_called_once()
