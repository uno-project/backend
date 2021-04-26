from uuid import uuid4
from typing import Dict, List, Tuple
from .player import Player
from .deck import Deck
from .cards import Card
from .exceptions import UnoRuleException, UnoWinnerException
import logging

MINIMUM_PLAYERS = 2
MAXIMUM_PLAYERS = 10
START_CARDS_HAND = 5


class Game:
    def __init__(self):
        logging.getLogger()
        self.id = uuid4().hex
        self.players = []
        self.deck = None
        self.playerToPlay = None
        self.__play_history = None
        self.notifications = []
        self.add_notification("addPlayer")

    def add_notification(self, message):
        a = 'data: '+message+'\n\n'
        self.notifications.append(a)

    def addPlayer(self, player: Player):
        # check if player already exists
        for p in self.players:
            if player.id == p.id:
                return True

        self.players.append(player)

        return True

    def start(self):
        if len(self.players) < MINIMUM_PLAYERS or len(self.players) > MAXIMUM_PLAYERS:
            raise UnoRuleException(
                f"Game needs at least two players and maximum ten")

        self.deck = Deck()
        self.deal_card()
        self.playerToPlay = 0
        self.__play_history = []

    def deal_card(self):
        for cards in range(START_CARDS_HAND):
            for player in self.players:
                player.addCard(self.deck.pickCard())

    def register_play(self, playerId: str, cardId: str, unoFlag=False):

        # get last player
        lastCard = Card()
        if len(self.__play_history) > 0:
            lastPlay = self.__play_history[-1]["card"]

        # player is not part of the game: error
        if playerId not in [p.id for p in self.players]:
            raise UnoRuleException(
                f"Player {playerId} does not belong to this game")

        # player to play
        playerToPlay = self.players[self.playerToPlay]

        # not players turn: raise error
        if playerId != playerToPlay.id:
            raise UnoRuleException(
                f"Player {playerId} should not play now. It's {playerToPlay.id}"
            )

        # uno flag not raised: punish
        if len(playerToPlay.cards) == 2 and unoFlag == False:
            playerToPlay.playCard(cardId)
            logging.info(f"Player {playerToPlay.id} forgot to ask uno")
            for i in range(2):
                playerToPlay.addCard(self.deck.pickCard())
            return self.__nextPlayer()

        # run actions from actual card based on last card
        try:
            # remove card from player
            card = playerToPlay.playCard(cardId)
            self.playerToPlay = card.actions(lastCard, self.playerToPlay,
                                             self.players, self.deck)

        except Exception as e:
            raise UnoRuleException(f"Error while playing card: {e}")

        # add history and run action
        self.__play_history.append({"player": playerId, "card": card})

        # player played last card: won
        if len(self.players[self.playerToPlay].cards) == 0:
            raise UnoWinnerException(
                f"Player {self.players[self.playerToPlay].id} is the winner")

        # next player
        return self.__nextPlayer()

    def __nextPlayer(self):
        if self.playerToPlay == len(self.players) - 1:
            self.playerToPlay = 0
        else:
            self.playerToPlay += 1

        return True
