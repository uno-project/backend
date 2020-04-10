from .cards import Card
from typing import Dict, List, Tuple

import logging

class Player:

    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def addCard(self, card: Card):
        self.cards.append(card)

    def playCard(self, card: Card):
        try:
            self.cards.remove(card)
        except Exception as e:
            logging.error(f"{card} not present")
