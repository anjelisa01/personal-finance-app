#strictly to test auth endpoint, 
#even tho in conftest do the same thing but dynamic
from fastapi.testclient import TestClient
from main import app
import uuid
client=TestClient(app)

def test_create_user(): 
    payload={
        "name": "test",
        "email": f"test_create_{uuid.uuid4().hex[:8]}@example.com",   #create new acc
        "password": "test",
        "currency":"usd"
        }
    response=client.post(
        "/api/v1/users/signup",
        json=payload)
    assert response.status_code==200

def test_login():
    payload={
        "username": "test@example.com", #this is an established test user
        "password":"test" 
        }
    response=client.post(
        '/api/v1/auth/login',
        data=payload)
    assert response.status_code==200
