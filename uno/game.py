from uuid import uuid4
from typing import Dict, List, Tuple
from .player import Player
from .deck import Deck
from .cards import Card

import logging

MINIMUM_PLAYERS = 2
MAXIMUM_PLAYERS = 10
START_CARDS_HAND = 5


class Game:
    def __init__(self, players: List[Player]):
        if len(players) < MINIMUM_PLAYERS or len(players) > MAXIMUM_PLAYERS:
            raise Exception(f"Game needs at least two players and maximum ten")

        logging.getLogger()
        self.id = uuid4().hex
        self.players = players
        self.deck = Deck()
        self.deal_card()
        self.playerToPlay = 0
        self.__play_history = []

    def deal_card(self):
        for cards in range(START_CARDS_HAND):
            for player in self.players:
                player.addCard(self.deck.pickCard())

    def register_play(self, playerId: str, card: Card, unoFlag=False):

        # get last player
        lastCard = Card()
        if len(self.__play_history) > 0:
            lastPlay = self.__play_history[-1]["card"]

        # not players turn: raise error
        if playerId != self.players[self.playerToPlay].id:
            raise Exception(
                f"Player {playerId} should not play now. It's {self.players[self.playerToPlay].id}"
            )

        # uno flag not raised: punish
        if len(self.players[
                self.playerToPlay].cards) == 1 and unoFlag == False:
            logging.info(
                f"Player {self.players[self.playerToPlay].id} forgot to ask uno"
            )
            for i in range(2):
                self.players[self.playerToPlay].addCard(self.deck.pickCard())
            return self.__nextPlayer()

        # run actions from actual card based on last card
        try:
            self.playerToPlay = card.actions(lastCard, self.playerToPlay,
                                             self.players, self.deck)

        except Exception as e:
            raise NotImplementedError(f"ARRUMA AQUI CARAIO: {e}")

        # add history and run action
        self.__play_history.append({"player": playerId, "card": card})

        # player played last card: won
        if len(self.players[self.playerToPlay].cards) == 0:
            raise Exception(
                f"Player {self.players[self.playerToPlay].id} is the winner")

        # next player
        return self.__nextPlayer()

    def __nextPlayer(self):
        if self.playerToPlay == len(self.players) - 1:
            self.playerToPlay = 0
        else:
            self.playerToPlay += 1

        return True
