from uuid import uuid4
from typing import Dict, List, Tuple
from .player import Player
from .deck import Deck

MINIMUM_PLAYERS = 2
MAXIMUM_PLAYERS = 10
START_CARDS_HAND = 5

class Game:

    def __init__(self, players: List[Player]):
        if len(players) < MINIMUM_PLAYERS or len(players) > MAXIMUM_PLAYERS:
            raise Exception(f"Game needs at least two players and maximum ten")

        self.id = uuid4().hex
        self.players = players
        self.deck = Deck()
        self.deal_card()
        self.__play_history = []

    def deal_card(self):
        for cards in range(START_CARDS_HAND):
            for player in self.players:
                player.addCard(self.deck.pickCard())
