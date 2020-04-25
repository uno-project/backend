from uno.cards import NumberedCard, PlusTwoCard, InvertedCard, JumpCard
from uno.cards import Card, JokerCard, JokerPlusFourCard
from uno.player import Player
from uno.deck import Deck
import pytest


def test_cards_actions():

    card = Card()
    with pytest.raises(NotImplementedError):
        card.actions("", "", "", "")


def test_numbered_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = NumberedCard(color="BLUE", number="1")
    card2 = NumberedCard(color="BLUE", number="2")
    card3 = NumberedCard(color="RED", number="2")

    # positive cases
    assert card2.actions(card1, 0, players, Deck()) == 0
    assert card3.actions(card2, 1, players, Deck()) == 1

    # negative case
    with pytest.raises(Exception):
        card3.actions(card1, 1, players, Deck())


def test_plustwo_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = PlusTwoCard(color="BLUE")
    card2 = PlusTwoCard(color="BLUE")
    card3 = PlusTwoCard(color="RED")

    assert card2.actions(card1, 0, players, Deck()) == 0
    assert len(player2.cards) == 2

    with pytest.raises(Exception):
        card3.actions(card1, 1, players, Deck())


def test_inverted_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = InvertedCard(color="BLUE")
    card2 = InvertedCard(color="BLUE")
    card3 = InvertedCard(color="RED")
    card4 = NumberedCard(color="BLUE", number="2")

    assert card2.actions(card1, 0, players, Deck()) == 1
    assert players == [player2, player1]
    assert card3.actions(card1, 1, players, Deck()) == 0
    assert players == [player1, player2]

    with pytest.raises(Exception):
        card3.actions(card4, 1, players, Deck())



def test_joker_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = JokerCard()
    card2 = JokerCard()
    card3 = NumberedCard(color="BLUE", number="1")

    card2.setColor("BLUE")
    assert card2.actions(card1, 0, players, Deck()) == 0
    assert card3.actions(card2, 0, players, Deck()) == 0

    with pytest.raises(Exception):
        card3.actions(card1, 1, players, Deck())


def test_jump_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = NumberedCard(color="BLUE", number="1")
    card2 = NumberedCard(color="RED", number="1")
    card3 = JumpCard(color="BLUE")

    assert card3.actions(card1, 0, players, Deck()) == 1
    assert card3.actions(card1, 1, players, Deck()) == 0

    with pytest.raises(Exception):
        card3.actions(card2, 1, players, Deck())


def test_jokerplusfour_actions():
    player1 = Player("player1")
    player2 = Player("player2")
    players = [player1, player2]

    card1 = JokerPlusFourCard()
    card2 = JokerPlusFourCard()
    card3 = NumberedCard(color="RED", number="1")
    card4 = NumberedCard(color="BLUE", number="1")

    card1.setColor(color="BLUE")
    assert card2.actions(card1, 0, players, Deck()) == 0
    assert len(player2.cards) == 4

    with pytest.raises(Exception):
        card3.actions(card1, 1, players, Deck())

    assert card4.actions(card1, 0, players, Deck()) == 0
