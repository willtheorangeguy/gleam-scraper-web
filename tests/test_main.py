from fastapi.testclient import TestClient

import app.main as main
from gleam_scraper.service import Competition


def test_api_competitions_supports_search(monkeypatch):
    monkeypatch.setattr(main, "init_database", lambda: None)
    monkeypatch.setattr(
        main,
        "list_competitions",
        lambda **_: [
            Competition("Alpha Prize", "https://gleam.io/giveaways/AAA11", "First"),
            Competition("Beta Prize", "https://gleam.io/giveaways/BBB22", "Second"),
        ],
    )

    with TestClient(main.app) as client:
        response = client.get("/api/competitions?q=beta")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Beta Prize"


def test_index_page_renders(monkeypatch):
    monkeypatch.setattr(main, "init_database", lambda: None)
    monkeypatch.setattr(
        main,
        "list_competitions",
        lambda **_: [Competition("Gamma Prize", "https://gleam.io/giveaways/CCC33", "")],
    )

    with TestClient(main.app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Gleam Competitions" in response.text
    assert "Gamma Prize" in response.text


def test_refresh_endpoint_redirects(monkeypatch):
    monkeypatch.setattr(main, "init_database", lambda: None)
    monkeypatch.setattr(main, "list_competitions", lambda **_: [])

    with TestClient(main.app) as client:
        response = client.post("/refresh", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/"

