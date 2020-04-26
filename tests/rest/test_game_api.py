import pytest
from unittest.mock import patch, MagicMock
from rest import create_app
import logging

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


def test_players_cards(server):
    gameId = create_game(server)
    players = server.get(f"/game/{gameId}").json['players']

    for playerId in players:
        req = server.get(f"/player/{playerId}")
        assert req.status_code == 200
        assert len(req.json["cards"]) == 5

def test_create_game_invalid_players(server):

    # add players
    player1Id = server.post("/player", json={
        "name": "player1"
    }).json["playerId"]

    req = server.post(f"/game", json={"players": [player1Id, "INVALID_ID"]})

    # assert game creation
    assert req.status_code == 404
    assert req.json["message"] == "Player INVALID_ID not found"


def test_play_invalid_gameId(server):
    gameId = create_game(server)

    # play with invalid pla
    req = server.put(f"/game/INVALID_ID",
                     json={
                         "playerId": "INVALID_ID",
                         "cardId": "INVALID_ID"
                     })

    assert req.status_code == 404


def test_play_invalid_player_and_card(server):
    gameId = create_game(server)

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={
                         "playerId": "INVALID_ID",
                         "cardId": "INVALID_ID"
                     })
    assert req.status_code == 400

def test_sucessful_play(server):
    gameId = create_game(server)

    # make user have one card
    player = server.application.config.games[gameId].players[0]

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={
                         "playerId": player.id,
                         "cardId": player.cards[0].id
                     })
    assert req.status_code == 200
    assert req.json["message"] == "success"

def test_winner(server):
    gameId = create_game(server)

    # make user have one card
    player = server.application.config.games[gameId].players[0]

    # set one card and play
    player.cards = player.cards[:1]

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={
                         "playerId": player.id,
                         "cardId": player.cards[0].id
                     })
    assert req.status_code == 200


def create_game(server):
    # add players
    player1Id = server.post("/player", json={
        "name": "player1"
    }).json["playerId"]
    player2Id = server.post("/player", json={
        "name": "player2"
    }).json["playerId"]

    # created succesful
    req = server.post(f"/game", json={"players": [player1Id, player2Id]})
    assert req.status_code == 200

    # get playersId and assert
    gameId = req.json["gameId"]
    req = server.get(f"/game/{gameId}")
    assert player1Id in req.json["players"]
    assert player2Id in req.json["players"]
    return gameId
