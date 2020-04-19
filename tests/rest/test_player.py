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

def test_index(server):
    req = server.get("/player/AAAA")

    # GET on / is not implemented
    assert req.status_code == 404

def test_create_player(server):

    # assert message error
    req = server.post("/player")
    assert req.status_code == 400

    # create player with name
    req = server.post("/player", json={"name": "ASDASDA"})
    assert req.status_code == 200
    assert "playerId" in req.json

    # assert player on GET
    req = server.get(f"/player/{req.json['playerId']}")
    assert req.status_code == 200
    assert req.json["name"] == "ASDASDA"
    assert req.json["cards"] == []

