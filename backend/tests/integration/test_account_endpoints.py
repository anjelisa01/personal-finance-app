import uuid

#this will make 3 records of accounts in db
#for create, read one, update test

def test_create_account(authenticated_client ):
    payload = {
        "account_name":f"test_create_{uuid.uuid4().hex[:8]}",
        "initial_balance":5000
    }
    response = authenticated_client.post(
        "/api/v1/accounts",
        json=payload,
    )
    assert response.status_code == 200

def test_read_one_account(authenticated_client,created_account):
    account_id=created_account["id"]
    response=authenticated_client.get(
        f"/api/v1/accounts/{account_id}")
    assert response.status_code==200

def test_read_all_accounts(authenticated_client):
    #this doenst use fixture created account since doesnt need account id
    response=authenticated_client.get(
        "/api/v1/accounts")
    assert response.status_code==200

def test_update_account(authenticated_client,created_account):
    account_id=created_account["id"]
    payload={
        "account_name": f"test_update_{uuid.uuid4().hex[:8]}",
        }
    response=authenticated_client.patch(
        f"/api/v1/accounts/{account_id}", 
        json=payload)
    assert response.status_code==200

def test_delete_account(authenticated_client,created_account):
    account_id=created_account["id"]
    response=authenticated_client.delete(
        f"/api/v1/accounts/{account_id}") 
    #this would not show up in db, since this account is deleted.
    assert response.status_code==200