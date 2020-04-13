from random import shuffle
from .cards import NumberedCard, PlusTwoCard, InvertedCard, JumpCard
from .cards import JokerCard, JokerPlusFourCard

# colors
COLORS = ("BLUE", "GREEN", "YELLOW", "RED")

# cards by color
NUMBER_RANGE = range(1, 10)
PLUS_TWO = range(2)
INVERT = range(2)
JUMP = range(2)

# no color
JOKER = range(4)
JOKER_PLUS_FOUR = range(4)

TOTAL_CARDS = 108


class Deck:
    """
    Represents the deck
    """
    def __init__(self):
        self.cards = []
        self.__generate_deck()
        self.shuffle()

    def __generate_deck(self):
        """
        Generate the initial 112 cards
        """
        # generate cards with colors
        for color in COLORS:

            # numbers
            self.cards.append(NumberedCard(color=color, number=0))
            for number in NUMBER_RANGE:
                self.cards.append(NumberedCard(color, number))
                self.cards.append(NumberedCard(color, number))

            # plus two cards
            for i in PLUS_TWO:
                self.cards.append(PlusTwoCard(color=color))

            # invert
            for i in INVERT:
                self.cards.append(InvertedCard(color=color))

            # jump cards
            for i in JUMP:
                self.cards.append(JumpCard(color=color))

        # generate ones without colors
        for i in JOKER:
            self.cards.append(JokerCard())

        for i in JOKER_PLUS_FOUR:
            self.cards.append(JokerPlusFourCard())

    def shuffle(self):
        shuffle(self.cards)

    def pickCard(self):
        return self.cards.pop()
