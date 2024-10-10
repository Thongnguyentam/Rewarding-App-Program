from constant import response_message
from tests.conftest import client
from fastapi import status

def create_add_payload(payer: str, points: int, timestamp: str):
    return {
        "payer":payer,
        "points":points,
        "timestamp":timestamp
    }
    
def spend_points(amount):
    payload = {"points" : amount}
    spend_response = client.post("/spend", json = payload)
    assert spend_response.status_code == status.HTTP_200_OK
    return spend_response

def add_points(payload):
    response = client.post("/add", json = payload)
    assert response.status_code == status.HTTP_200_OK
    
def get_balance():
    balance_response = client.get("/balance")
    assert balance_response.status_code == status.HTTP_200_OK, balance_response.text
    return balance_response.json()
    
def test_add_positive_points():
    payload = create_add_payload("DANNON", 5000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    data = get_balance()
    assert data.get("DANNON") == 5000
    
def test_add_negative_points_leads_to_positive_points_by_payer():
    payload = create_add_payload("DANNON", 5000, "2020-11-02T14:00:00Z")
    add_points(payload)
    payload = create_add_payload("DANNON", -4000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    data = get_balance()
    assert data.get("DANNON") == 1000
    
def test_add_negative_points_leads_to_negative_points_by_payer():
    payload = create_add_payload("DANNON", 5000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    payload = create_add_payload("DANNON", -6000, "2020-11-02T14:00:00Z")
    response = client.post("/add", json = payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = get_balance()
    assert data.get("DANNON") == 5000
    
def test_spend_points_when_single_payer_has_sufficient_points():
    payload = create_add_payload("DANNON", 5000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    spend_points(amount = 4000)
    
    data = get_balance()
    assert data.get("DANNON") == 1000
    
def test_spend_all_points_single_payer_across_one_record():
    payload = create_add_payload("DANNON", 5000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    spend_points(amount = 5000)
    
    data = get_balance()
    assert data.get("DANNON") == 0

def test_spend_one_payer_multiple_rows():
    payload = create_add_payload("DANNON", 5000, "2020-11-03T14:00:00Z")
    add_points(payload)
    payload = create_add_payload("DANNON", 2000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    spend_response = spend_points(amount = 4700)
    data = spend_response.json()[0]
    assert data["payer"] == "DANNON"
    assert data["points"] == -4700
    
    data = get_balance()
    assert data.get("DANNON") == 2300

def test_2_payer_mutiple_spent_rows():
    payload = create_add_payload("DANNON", 5000, "2020-11-04T14:00:00Z")
    add_points(payload)
    payload = create_add_payload("UNILEVER", 1000, "2020-11-03T14:00:00Z")
    add_points(payload)
    payload = create_add_payload("DANNON", 2000, "2020-11-02T14:00:00Z")
    add_points(payload)
    
    spend_response = spend_points(1000)
    data = spend_response.json()[0]
    assert data["payer"] == "DANNON"
    assert data["points"] == -1000
    
    data = get_balance()
    assert data.get("DANNON") == 6000
    
    spend_response = spend_points(1800)
    data = spend_response.json()[0]
    assert data["payer"] == "DANNON"
    assert data["points"] == -1000
    data = spend_response.json()[1]
    assert data["payer"] == "UNILEVER"
    assert data["points"] == -800
    
    data = get_balance()
    assert data.get("DANNON") == 5000
    assert data.get("UNILEVER") == 200
    
    spend_response = spend_points(2200)
    data = spend_response.json()[0]
    assert data["payer"] == "DANNON"
    assert data["points"] == -2000
    data = spend_response.json()[1]
    assert data["payer"] == "UNILEVER"
    assert data["points"] == -200
    
    data = get_balance()
    assert data.get("DANNON") == 3000
    assert data.get("UNILEVER") == 0
    
def test_spend_more_than_having_one_payer():
    payload = create_add_payload("DANNON", 5000, "2020-11-03T14:00:00Z")
    add_points(payload)
    
    payload = {"points" : 6000}
    spend_response = client.post("/spend", json = payload)
    assert spend_response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = get_balance()
    assert data.get("DANNON") == 5000
    
def test_spend_more_than_having_two_payers():
    payload = create_add_payload("DANNON", 5000, "2020-11-04T14:00:00Z")
    add_points(payload)
    payload = create_add_payload("UNILEVER", 1000, "2020-11-04T14:00:00Z")
    add_points(payload)
    
    payload = {"points" : 7000}
    spend_response = client.post("/spend", json = payload)
    assert spend_response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = get_balance()
    assert data.get("DANNON") == 5000
    assert data.get("UNILEVER") == 1000
    
def test_multiple_payer_multiple_rows():
    p1 = create_add_payload("DANNON", 300, "2022-10-31T10:00:00Z")
    p2 = create_add_payload("UNILEVER", 200, "2022-10-31T11:00:00Z")
    p3 = create_add_payload("DANNON", -200, "2022-10-31T15:00:00Z")
    p4 = create_add_payload("MILLER COORS", 10000, "2022-11-01T14:00:00Z")
    p5 = create_add_payload("DANNON", 1000, "2022-11-02T14:00:00Z")
    payloads = [p1,p2,p3,p4,p5]
    
    for payload in payloads:
        add_points(payload)
    
    data = get_balance()
    assert data.get("DANNON") == 1100
    assert data.get("MILLER COORS") == 10000
    assert data.get("UNILEVER") == 200
    
    spend_points(5000)
    data = get_balance()
    assert data.get("DANNON") == 1000
    assert data.get("MILLER COORS") == 5300
    assert data.get("UNILEVER") == 0
    
def test_add_points_with_invalid_timestamp():
    # Invalid timestamp format
    payload = create_add_payload("DANNON", 5000, "invalid-timestamp")
    response = client.post("/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

def test_add_points_missing_required_fields():
    # Missing the 'payer' field
    payload = {
        "points": 5000,
        "timestamp": "2020-11-02T14:00:00Z"
    }
    response = client.post("/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "payer" in response.json()["detail"][0]["loc"], "Payer validation error not raised"
    
    # Missing the 'points' field
    payload = {
        "payer": "DANNON",
        "timestamp": "2020-11-02T14:00:00Z"
    }
    response = client.post("/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "points" in response.json()["detail"][0]["loc"]

def test_add_points_with_invalid_points_type():
    payload = create_add_payload("DANNON", "invalid_points", "2020-11-02T14:00:00Z")
    response = client.post("/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "points" in response.json()["detail"][0]["loc"]

    