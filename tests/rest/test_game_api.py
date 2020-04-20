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

def test_game_index(server):
    req = server.get("/game/AAAA")

    # GET on / is not implemented
    assert req.status_code == 404

def test_create_game(server):

    # add players
    player1Id = server.post("/player", json={"name": "player1"}).json["playerId"]
    player2Id = server.post("/player", json={"name": "player2"}).json["playerId"]

    req = server.post(f"/game", json={"players": [player1Id, player2Id]})

    # assert game creation
    assert req.status_code == 200
    assert "gameId" in req.json
    req = server.get(f"/game/{req.json['gameId']}")
    assert player1Id in req.json["players"]
    assert player2Id in req.json["players"]

def test_create_game_invalid_players(server):

    # add players
    player1Id = server.post("/player", json={"name": "player1"}).json["playerId"]

    req = server.post(f"/game", json={"players": [player1Id, "INVALID_ID"]})

    # assert game creation
    assert req.status_code == 404
    assert req.json["message"] == "Player INVALID_ID not found"

