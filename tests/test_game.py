from uno.game import Game
from uno.player import Player
from uno.cards import NumberedCard, Card
from uuid import UUID
import pytest

DECK_SIZE = 108
STARTING_CARDS = 5

game = None
player1 = None
player2 = None


def test_game_initial():
    global player1
    global player2
    player1 = Player("player1")
    player2 = Player("player2")

    # start game
    global game
    game = Game(players=[player1, player2])

    # if game.id is not a UUID, will throw exception
    assert isinstance(UUID(game.id), UUID)

    assert len(game.deck.cards) == int(DECK_SIZE - (2 * STARTING_CARDS))

    for player in game.players:
        assert len(player.cards) == STARTING_CARDS


def test_play_first_card():
    global player1
    global player2
    global game

    # pick a card and assert
    player1.playCard(player1.cards[0])
    assert len(player1.cards) == 4

    # player1 play random card
    blue = NumberedCard(color="BLUE", number="1")
    assert game.register_play(player1.id, blue)


def test_play_wrong_player():
    global player1
    global player2
    global game

    # try to play with
    blue = NumberedCard(color="BLUE", number="1")
    with pytest.raises(Exception):
        game.register_play(player1.id, blue)
    assert len(game._Game__play_history) == 1
    assert game.playerToPlay == 1


def test_play_player2():
    global player1
    global player2
    global game

    blue = NumberedCard(color="BLUE", number="1")
    assert game.register_play(player2.id, blue)


def test_play_player1_forget_uno():
    global player1
    global player2
    global game

    blue = NumberedCard(color="BLUE", number="1")
    player1.cards = player1.cards[:1]

    game.register_play(player1.id, blue)

    # check penalty
    assert len(player1.cards) == 3
    assert game.playerToPlay == 1


def test_play_player2_remember_uno():
    global player1
    global player2
    global game

    blue = NumberedCard(color="BLUE", number="1")
    player2.cards = player2.cards[:1]

    assert game.register_play(player2.id, blue, unoFlag=True)


def test_play_player1_winner():
    global player1
    global player2
    global game

    blue = NumberedCard(color="BLUE", number="1")
    player1.cards = []

    assert not isinstance(player1.playCard(blue), Card)

    with pytest.raises(Exception):
        game.register_play(player1.id, blue)

    # check penalty
    assert len(player1.cards) == 0
