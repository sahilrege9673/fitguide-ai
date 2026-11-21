def test_list_exercises_count_and_pagination(client):
    res = client.get("/api/v1/exercises?page=1&page_size=100")
    assert res.status_code == 200
    data = res.json()
    assert data["total_records"] >= 80
    assert len(data["data"]) >= 80
    assert data["page"] == 1

def test_filter_exercises_by_category(client):
    res = client.get("/api/v1/exercises?category=strength")
    assert res.status_code == 200
    data = res.json()
    assert len(data["data"]) > 0
    assert all(e["category"] == "strength" for e in data["data"])

def test_filter_exercises_by_muscle(client):
    res = client.get("/api/v1/exercises?muscle=chest")
    assert res.status_code == 200
    data = res.json()
    assert len(data["data"]) > 0
    assert any("chest" in m for e in data["data"] for m in e["primary_muscles"])

def test_filter_exercises_by_equipment(client):
    res = client.get("/api/v1/exercises?equipment=barbell")
    assert res.status_code == 200
    data = res.json()
    assert len(data["data"]) > 0
    assert all("barbell" in e["equipment_needed"] for e in data["data"])

def test_get_exercise_by_slug(client):
    res = client.get("/api/v1/exercises/barbell-back-squat")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Barbell Back Squat"
    assert "quadriceps" in data["primary_muscles"]
    assert len(data["media"]) > 0
    assert "Victor Freitas" in data["media"][0]["attribution_text"]

def test_get_exercise_non_existent_404(client):
    res = client.get("/api/v1/exercises/unknown-exercise-slug")
    assert res.status_code == 404
