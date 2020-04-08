from uno.deck import Deck
from uno.cards import NumberedCard, PlusTwoCard, InvertedCard, JumpCard
from uno.cards import JokerCard, JokerPlusFourCard, BlankJokerCard, JokerChangeHands

import pytest


def test_deck_generation():
    deck = Deck()

    # deck should have 112 cards
    assert (len(deck.cards) == 112)

    instancesNCounters = {
        NumberedCard: 76,
        PlusTwoCard: 8,
        InvertedCard: 8,
        JumpCard: 8,
        JokerCard: 4,
        JokerPlusFourCard: 4,
        BlankJokerCard: 3,
        JokerChangeHands: 1
    }

    for card in deck.cards:

        for instance in instancesNCounters.keys():
            if isinstance(card, instance) is True:
                instancesNCounters[instance] -= 1
                break

    # verify if deck is completed checked
    for instance in instancesNCounters.keys():
        assert instancesNCounters[
            instance] == 0, f"{instance} has incorrect number"
