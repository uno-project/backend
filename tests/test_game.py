from uno.game import Game
from uno.player import Player

from uuid import UUID
import pytest

DECK_SIZE = 112
STARTING_CARDS = 5

def test_game_initial():
    player1 = Player("player1")
    player2 = Player("player2")

    # start game
    game = Game(players=[player1, player2])

    # if game.id is not a UUID, will throw exception
    assert isinstance(UUID(game.id), UUID)

    assert len(game.deck.cards) == int(DECK_SIZE-(2*STARTING_CARDS))

    for player in game.players:
        assert len(player.cards) == STARTING_CARDS

