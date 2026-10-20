import uuid

def test_create_category(authenticated_client):
    payload={
        "category_name": f"test_create_{uuid.uuid4().hex[:8]}",
        "category_type":"expense"}

    response=authenticated_client.post(
        "/api/v1/categories",
        json=payload)
    assert response.status_code==200

def test_read_one_category(authenticated_client,created_category):
    category_id=created_category['id']
    response=authenticated_client.get(
        f"/api/v1/categories/{category_id}") #category_id has to belong to the authenticated client
    assert response.status_code==200

def test_read_all_categories(authenticated_client):
    response=authenticated_client.get(
        "/api/v1/categories")
    assert response.status_code==200

def test_update_category(authenticated_client,created_category):
    category_id=created_category['id']
    payload={
        "category_name": f"test_update_{uuid.uuid4().hex[:8]}",
        }
    response=authenticated_client.patch(
        f"/api/v1/categories/{category_id}", #category_id has to belong to the authenticated client
        json=payload) 
    assert response.status_code==200

def test_delete_category(authenticated_client,created_category):
    category_id=created_category['id']
    response=authenticated_client.delete(
        f"/api/v1/categories/{category_id}") #category_id has to belong to the authenticated client
    assert response.status_code==200