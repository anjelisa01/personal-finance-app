
def test_read_one_user(authenticated_client):
    response=authenticated_client.get("/api/v1/users/me")
    assert response.status_code==200

def test_update_user(authenticated_client):
    payload={
        "name": "jobe",   
        }
    response=authenticated_client.patch(
        "/api/v1/users/me",
        json=payload)
    assert response.status_code==200


#this delete the test account 
#its working but dont run again
# def test_delete_user(authenticated_client):
#     response=authenticated_client.delete("/api/v1/users/me")
#     assert response.status_code==200