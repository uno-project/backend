import pytest
import logging

from unittest.mock import patch, MagicMock

from rest import create_app
from tests.rest.test_player_api import create_player


@pytest.fixture()
def server():
    # start app
    app = create_app()
    app.config['TESTING'] = True

    server = app.test_client()

    yield server


def test_invalid_gameId(server):
    gameInfo = create_game(server)
    token = gameInfo["players"][0]["token"]
    req = server.get("/game/AAAA",
                     headers={"Authorization": f"Bearer {token}"})

    assert req.status_code == 404


def test_players_cards(server):
    gameInfo = create_game(server)

    # assert player1 cards
    for player in gameInfo["players"]:
        req = server.get(
            f"/player", headers={"Authorization": f"Bearer {player['token']}"})
        assert req.status_code == 200
        assert len(req.json["cards"]) == 5


def test_create_game_invalid_players(server):

    # add players
    player, token = create_player("player1", server)
    req = server.post(f"/game",
                      json={"players": [player, "INVALID_ID"]},
                      headers={"Authorization": f"Bearer {token}"})

    # assert game creation
    assert req.status_code == 404
    assert req.json["message"] == "Player INVALID_ID not found"


def test_play_invalid_game(server):
    gameInfo = create_game(server)
    token = gameInfo["players"][0]["token"]

    # play with invalid player
    req = server.put(f"/game/INVALID_ID",
                     json={"cardId": "INVALID_ID"},
                     headers={"Authorization": f"Bearer {token}"})

    assert req.status_code == 404


def test_wrong_player(server):
    gameInfo = create_game(server)
    gameId = gameInfo["game"]
    token = gameInfo["players"][1]["token"]

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={"cardId": "ID"},
                     headers={"Authorization": f"Bearer {token}"})
    assert req.status_code == 400


def test_sucessful_play(server):
    gameInfo = create_game(server)
    gameId = gameInfo["game"]
    token = gameInfo["players"][0]["token"]

    # make user have one card
    player = server.application.config.games[gameId].players[0]

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={"cardId": player.cards[0].id},
                     headers={"Authorization": f"Bearer {token}"})
    assert req.status_code == 200
    assert req.json["message"] == "success"


def test_winner(server):
    gameInfo = create_game(server)
    gameId = gameInfo["game"]
    token = gameInfo["players"][0]["token"]

    # make user have one card
    player = server.application.config.games[gameId].players[0]

    # set one card and play
    player.cards = player.cards[:1]

    # play with invalid pla
    req = server.put(f"/game/{gameId}",
                     json={"cardId": player.cards[0].id},
                     headers={"Authorization": f"Bearer {token}"})
    assert req.status_code == 200


def create_game(server):
    # add players
    player1, token1 = create_player("player1", server)
    player2, token2 = create_player("player2", server)

    # created succesful
    req = server.post(f"/game",
                      json={"players": [player1, player2]},
                      headers={"Authorization": f"Bearer {token1}"})
    assert req.status_code == 200

    # get playersId and assert
    gameId = req.json["gameId"]
    req = server.get(f"/game/{gameId}",
                     headers={"Authorization": f"Bearer {token1}"})

    assert player1 in req.json["players"]
    assert player2 in req.json["players"]
    return {
        "game":
        gameId,
        "players": [{
            "player": player1,
            "token": token1
        }, {
            "player": player2,
            "token": token2
        }]
    }
