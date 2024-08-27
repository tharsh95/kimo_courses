from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_course_overview():
    response = client.get("/courses/Introduction%20to%20Deep%20Learning")
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) > 0
    
    first_item = response_json[0]
    assert "name" in first_item
    assert "description" in first_item

def test_get_specific_chapter():
    response = client.get("/courses/Introduction%20to%20Deep%20Learning/chapters/Deep%20Learning%20New%20Frontiers")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "text" in response.json()

# def test_rate_chapter():
#     response = client.post("/courses//chapters/Deep%20Learning%20New%20Frontiers/rate", json={"rating": 9})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Rating added successfully"
