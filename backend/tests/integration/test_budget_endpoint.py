#user - category - budget
def test_create_budget(authenticated_client,created_category):
    category_id=created_category['id']
    payload={
            "amount": 200,
            "period":"monthly"
    }
    response=authenticated_client.post(
        f"/api/v1/categories/{category_id}/budget",
        json=payload,
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code==200

def test_read_one_budget(authenticated_client,created_budget):
    category_id = created_budget["category_id"]
    
    response=authenticated_client.get(
        f"/api/v1/categories/{category_id}/budget")
    assert response.status_code==200




def test_update_budget(authenticated_client,created_budget):
    category_id = created_budget["category_id"]
    payload={
        "amount": "5000", # change
        }
    response=authenticated_client.patch(
        f"/api/v1/categories/{category_id}/budget",
        json=payload)
    assert response.status_code==200

#dont need to provide budget id, since category and budget is 1to1, so select by category id is enough
def test_delete_budget(authenticated_client,created_budget):
    category_id = created_budget["category_id"]
    response=authenticated_client.delete(
        f"/api/v1/categories/{category_id}/budget")
    assert response.status_code==200    