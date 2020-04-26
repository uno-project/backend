import pytest
from unittest.mock import patch, MagicMock
from rest import create_app


@pytest.fixture()
def server():
    # start app
    app = create_app()
    app.config['TESTING'] = True

    server = app.test_client()

    yield server


def test_not_logged(server):
    req = server.get("/player/AAAA")
    assert req.status_code == 401


def test_create_player(server):
    playerId, token = create_player("ASDASDA", server)

    # assert player on GET
    req = server.get("/player", headers={"Authorization":f"Bearer {token}"})
    assert req.status_code == 200
    assert req.json["name"] == "ASDASDA"
    assert req.json["cards"] == []


def create_player(name, server):
    # create player with name
    req = server.post("/player", json={"name": name})
    assert req.status_code == 200

    # login
    playerId = req.json["playerId"]
    req = server.post("/login", json={"playerId": playerId,
                                      "playerName": name})

    # get token
    assert "access_token" in req.json
    token = req.json["access_token"]

    return playerId, token
