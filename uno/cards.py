class Card:
    """
    Represents the card in the game
    """
    def __actions(self):
        raise NotImplementedError()

class NumberedCard(Card):
    def __init__(self, color, number):
        self.color = color
        self.number = number

class PlusTwoCard(Card):
    def __init__(self, color):
        self.color = color

class InvertedCard(Card):
    def __init__(self, color):
        self.color = color

class JumpCard(Card):
    def __init__(self, color):
        self.color = color


class JokerCard(Card):
    pass

class JokerPlusFourCard(Card):
    pass

class JokerChangeHands(Card):
    pass

class BlankJokerCard(Card):
    pass
