from .cards import Card
from typing import Dict, List, Tuple

from uuid import uuid4
import logging


class Player:
    def __init__(self, name: str):
        self.id = uuid4().hex
        self.name = name
        self.cards = []

    def addCard(self, card: Card):
        self.cards.append(card)

    def playCard(self, card: Card):
        try:
            return self.cards.remove(card)
        except Exception as e:
            logging.error(f"{card} not present")
