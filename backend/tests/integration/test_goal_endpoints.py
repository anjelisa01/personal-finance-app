import uuid

def test_create_goal(authenticated_client):
    payload={
            "goal_name":f"test_create_{uuid.uuid4().hex[:8]}",
            "target_amount":1800,
            "due_date":"2027-03-22" 
            }
    response=authenticated_client.post(
        "/api/v1/goals",
        json=payload)
    assert response.status_code==200

def test_read_one_goal(authenticated_client,created_goal):
    goal_id=created_goal["id"]
    response=authenticated_client.get(
        f"/api/v1/goals/{goal_id}") #goal id has to be existed for authentucated client
    assert response.status_code==200

def test_read_all_goals(authenticated_client):
    response=authenticated_client.get(
        "/api/v1/goals")
    assert response.status_code==200

def test_update_goal(authenticated_client,created_goal):
    goal_id=created_goal["id"]
    payload={
        "goal_name":f"test_update_{uuid.uuid4().hex[:8]}"
        }
    response=authenticated_client.patch(
        f"/api/v1/goals/{goal_id}",
        json=payload)
    assert response.status_code==200

def test_delete_goal(authenticated_client,created_goal):
    goal_id=created_goal["id"]
    response=authenticated_client.delete(
        f"/api/v1/goals/{goal_id}")
    assert response.status_code==200