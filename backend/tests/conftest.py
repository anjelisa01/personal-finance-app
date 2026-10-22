import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def authenticated_client():
    client=TestClient(app)
    payload={
        "username": "test@example.com",
        "password":"test" 
        }
    response=client.post(
        '/api/v1/auth/login',
        data=payload)
    print(response.status_code)
    print(response.json())  # Shows why validation failed
    assert response.status_code==200

    token=response.json()["access_token"]

    client.headers.update({
        "Authorization":f"Bearer {token}"
    })
    return client

import uuid
@pytest.fixture
def created_account(authenticated_client):
    payload={
        "account_name":f"test_fixture_read1_{uuid.uuid4().hex[:8]}", #generating new name for every test
        "initial_balance":5000
    }
    #if in db test_fixture_read1 is present thats from read_one_account test
    #if changed its from update account test
    response=authenticated_client.post(
        "/api/v1/accounts",
        json=payload,
    )
    assert response.status_code == 200, response.text
    return response.json()

@pytest.fixture
def created_category(authenticated_client):
    payload={
        "category_name":f"test_fixture_read1_{uuid.uuid4().hex[:8]}", #generating new name for every test
        "category_type":"expense"
    }
    #if in db test_fixture_read1 is present thats from read_one_account test
    #if changed its from update category test
    response=authenticated_client.post(
        "/api/v1/categories",
        json=payload,
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest.fixture
def created_goal(authenticated_client):
    payload={
            "goal_name":f"test_fixture_read1_{uuid.uuid4().hex[:8]}",
            "target_amount":1800,
            "due_date":"2027-03-22" 
            }
    response=authenticated_client.post(
        "/api/v1/goals",
        json=payload,
    )
    assert response.status_code == 200, response.text
    return response.json()

#authenticated client - make category - make budget
@pytest.fixture
def created_budget(authenticated_client,created_category):
    category_id=created_category['id']
    payload={
            "amount": 200,
            "period":"monthly"
    }
    response=authenticated_client.post(
        f"/api/v1/categories/{category_id}/budget",
        json=payload,
    )
    return response.json()


#bare minimum transaction
#authenticated client - make category - make budget
@pytest.fixture
def created_transaction(authenticated_client,created_account,):
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
    return response.json()








'''

import pytest
from fastapi.testclient import TestClient
from main import app
# import logging

# logging.getLogger("httpx").setLevel(logging.WARNING)

@pytest.fixture
def authenticated_client():
    client=TestClient(app)
    payload={
        "email": "erling@example.com",
        "password":"erling" 
        }
    response=client.post(
        '/api/v1/auth/login',
        json=payload)
    
    assert response.status_code==200

    token=response.json()["access_token"]

    client.headers.update({
        "Authorization":f"Bearer {token}"
    })
    return client
        


# #kalo mau pake db asli, comment all of this file

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# TEST_DATABASE_URL="sqlite:///./test.db"

# test_engine=create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread":False}
# )

# TestingSessionLocal=sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=test_engine
# )


# from main import app
# from database import Base
# from dependency import get_db

# Base.metadata.create_all(bind=test_engine)

# def override_get_db():
#     db=TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db]=override_get_db

'''