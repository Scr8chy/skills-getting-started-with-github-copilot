import uuid
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def get_participants(activity_name: str):
    resp = client.get("/activities")
    resp.raise_for_status()
    data = resp.json()
    return data[activity_name]["participants"]


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity check: known activity is present
    assert "Chess Club" in data

import uuid
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def get_participants(activity_name: str):
    resp = client.get("/activities")
    resp.raise_for_status()
    data = resp.json()
    return data[activity_name]["participants"]


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity check: known activity is present
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = f"test-{uuid.uuid4()}@example.com"

    # ensure email not present
    participants = get_participants(activity)
    assert email not in participants

    # sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # verify present
    participants = get_participants(activity)
    assert email in participants

    # remove
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 200
    assert "Removed" in r.json().get("message", "")

    # verify removed
    participants = get_participants(activity)
    assert email not in participants


def test_duplicate_signup_returns_400():
    activity = "Programming Class"
    email = f"dup-{uuid.uuid4()}@example.com"

    # first signup ok
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    # second signup should fail with 400
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400

    # cleanup: remove participant
    r3 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r3.status_code == 200


def test_remove_nonexistent_participant_returns_404():
    activity = "Gym Class"
    email = f"nope-{uuid.uuid4()}@example.com"

    # make sure email is not present
    participants = get_participants(activity)
    assert email not in participants

    # attempt to remove -> 404
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 404