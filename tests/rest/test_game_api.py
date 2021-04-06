import pytest
import logging

from unittest.mock import patch, MagicMock
from http import HTTPStatus

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

    assert req.status_code == HTTPStatus.NOT_FOUND


def test_players_cards(server):
    gameInfo = create_game(server)

    # assert player1 cards
    for player in gameInfo["players"]:
        req = server.get(
            f"/player", headers={"Authorization": f"Bearer {player['token']}"})
        assert req.status_code == HTTPStatus.OK
        assert len(req.json["cards"]) == 5


def test_create_game_not_enough_players(server):

    # create game
    token = create_player("player1", server)
    gameId = create_only_game(token, server)

    # start game
    req = server.patch(f"/game/{gameId}",
                     json={"players": [server.get("/player",
                                            headers={"Authorization": f"Bearer {token}"}).json["id"]]},
                      headers={"Authorization": f"Bearer {token}"})

    # assert game creation
    assert req.status_code == 400
    assert req.json["message"] == "Game needs at least two players and maximum ten"

def test_create_game_invalid_players(server):

    # create game
    token = create_player("player1", server)
    gameId = create_only_game(token, server)

    # start game
    req = server.patch(f"/game/{gameId}",
                     json={"players": [server.get("/player",
                                            headers={"Authorization": f"Bearer {token}"}).json["id"],
                                            "INVALID_ID"]},
                      headers={"Authorization": f"Bearer {token}"})

    # assert game creation
    assert req.status_code == HTTPStatus.NOT_FOUND
    assert req.json["message"] == "Player INVALID_ID not found"


def test_play_invalid_game(server):
    gameInfo = create_game(server)
    token = gameInfo["players"][0]["token"]

    # play with invalid player
    req = server.put(f"/game/INVALID_ID",
                     json={"cardId": "INVALID_ID"},
                     headers={"Authorization": f"Bearer {token}"})

    assert req.status_code == HTTPStatus.NOT_FOUND


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
    assert req.status_code == HTTPStatus.OK
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
    assert req.status_code == HTTPStatus.OK


def create_only_game(token, server):
    # created succesful
    req = server.post(f"/game",
                      headers={"Authorization": f"Bearer {token}"})
    assert req.status_code == HTTPStatus.CREATED
    return req.json["gameId"]


def create_game(server):
    # add players
    token1 = create_player("player1", server)
    token2 = create_player("player2", server)

    gameId = create_only_game(token1, server)

    # start game
    req = server.patch(f"/game/{gameId}",
                     json={"players": [server.get("/player",
                                            headers={"Authorization": f"Bearer {token1}"}).json["id"],
                                        server.get("/player",
                                            headers={"Authorization": f"Bearer {token2}"}).json["id"]]},
                      headers={"Authorization": f"Bearer {token1}"})


    # get playersId and assert
    req = server.get(f"/game/{gameId}",
                     headers={"Authorization": f"Bearer {token1}"})

    return {
        "game":
        gameId,
        "players": [{
            "token": token1
        }, {
            "token": token2
        }]
    }
