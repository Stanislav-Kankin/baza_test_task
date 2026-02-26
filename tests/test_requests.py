
import threading
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_and_assign():
    # create
    r = client.post("/requests/?client_name=Test&phone=1&address=A&problem_text=P")
    request_id = r.json()["id"]

    # assign to master id 2
    client.post(f"/requests/{request_id}/assign/2")
    return request_id


def test_successful_take():
    request_id = create_and_assign()
    response = client.post(f"/requests/{request_id}/take/2")
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_race_take():
    request_id = create_and_assign()

    results = []

    def take():
        r = client.post(f"/requests/{request_id}/take/2")
        results.append(r.status_code)

    t1 = threading.Thread(target=take)
    t2 = threading.Thread(target=take)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert 200 in results
    assert 409 in results
