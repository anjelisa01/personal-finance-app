def test_create_transaction_minimum(authenticated_client,created_account):
    account_id=created_account['id']
    payload={
            "title": "test_fixture_created_transaction_minimal",
            "amount": 500,
            "note": "a test transaction",
            "category_id": 0, #no category
            "transaction_type": "expense",
            # "transfer_id": 0, #not a transfer
            # "transfer_direction": "incoming" #not a transfer
            }
    response=authenticated_client.post(
        f"/api/v1/accounts/{account_id}/transactions",
        json=payload,
    )
    assert response.status_code==200
#add create transaction: expense, income,transfer, with cat id


def test_read_one_transaction(authenticated_client,created_transaction):
    account_id=created_transaction['account_id']
    transaction_id=created_transaction['id']
    response=authenticated_client.get(
        f"/api/v1/accounts/{account_id}/transactions/{transaction_id}")
    assert response.status_code==200

def test_read_all_transaction(authenticated_client,created_transaction):
    account_id=created_transaction['account_id']
    response=authenticated_client.get(
        f"/api/v1/accounts/{account_id}/transactions")
    assert response.status_code==200

def test_update_transaction(authenticated_client,created_transaction):
    account_id=created_transaction['account_id']
    transaction_id=created_transaction['id']
    payload={
        "title": "i changed", # change category id to 3, oreviously null(default)
        }
    response=authenticated_client.patch(
        f"/api/v1/accounts/{account_id}/transactions/{transaction_id}",
        json=payload)
    
    assert response.status_code==200
 
def test_delete_transaction(authenticated_client,created_transaction):
    account_id=created_transaction['account_id']
    transaction_id=created_transaction['id']
    response=authenticated_client.delete(f"/api/v1/accounts/{account_id}/transactions/{transaction_id}")
    assert response.status_code==200
