from uno.exceptions import UnoRuleException, UnoWinnerException
from uno.game import Game
from uno.player import Player
from uno.cards import NumberedCard, Card
from uuid import UUID
import pytest

DECK_SIZE = 108
STARTING_CARDS = 5

game = None


def test_game_initial():
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


def test_game_one_or_ten_players():
    # 1 player: error
    player1 = Player("player1")
    with pytest.raises(UnoRuleException):
        game = Game(players=[player1])

    # 11 players: error
    players = [Player(f"player{i}") for i in range(11)]
    with pytest.raises(UnoRuleException):
        game = Game(players=[players])


def test_play_invalid_id():
    global game
    player1 = game.players[0]

    with pytest.raises(UnoRuleException):
        assert game.register_play("INVALID", "INVALID")

def test_play_first_card():
    global game
    player1 = game.players[0]

    # pick a card and assert
    player1.playCard(player1.cards[0].id)
    assert len(player1.cards) == 4

    # player1 play random card
    blue = NumberedCard(color="BLUE", number="1")
    player1.addCard(blue)
    assert game.register_play(player1.id, blue.id)


def test_play_wrong_player():
    global game
    player1 = game.players[0]

    # add card to player
    player1.playCard(player1.cards[0].id)
    blue = NumberedCard(color="BLUE", number="1")
    player1.addCard(blue)

    # play card
    with pytest.raises(UnoRuleException):
        game.register_play(player1.id, blue.id)
    assert len(game._Game__play_history) == 1
    assert game.playerToPlay == 1


def test_play_wrong_card():
    global game
    player2 = game.players[1]

    # play card
    with pytest.raises(UnoRuleException):
        game.register_play(player2.id, "WRONGID")
    assert len(game._Game__play_history) == 1
    assert game.playerToPlay == 1


def test_play_player2():
    global game
    player2 = game.players[1]

    player2.playCard(player2.cards[0].id)
    blue = NumberedCard(color="BLUE", number="1")
    player2.addCard(blue)
    assert game.register_play(player2.id, blue.id)


def test_play_player1_forget_uno():
    global game
    player1 = game.players[0]

    blue = NumberedCard(color="BLUE", number="1")
    player1.cards = player1.cards[:1]
    player1.addCard(blue)

    game.register_play(player1.id, blue.id)

    # check penalty
    assert len(player1.cards) == 3
    assert game.playerToPlay == 1


def test_play_player2_remember_uno():
    global game
    player2 = game.players[1]

    blue = NumberedCard(color="BLUE", number="1")
    player2.cards = player2.cards[:1]
    player2.addCard(blue)

    assert game.register_play(player2.id, blue.id, unoFlag=True)


def test_play_player1_winner():
    global game
    player1 = game.players[0]

    blue = NumberedCard(color="BLUE", number="1")
    player1.cards = [blue]

    with pytest.raises(UnoWinnerException):
        game.register_play(player1.id, blue.id)

    # check penalty
    assert len(player1.cards) == 0
