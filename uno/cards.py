class Card:
    """
    Represents the card in the game
    """
    def __init__(self, color=None, number=None):
        self.color = color
        self.number = number

    def actions(self, lastCard, indexPlayer, players, deck):
        raise NotImplementedError()


class NumberedCard(Card):
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def actions(self, lastCard, indexPlayer, players, deck):
        # same color as last card: success
        if lastCard.color not in [self.color, None
                                  ] and lastCard.number != self.number:
            raise Exception("Card must be same color or number")

        return indexPlayer


class PlusTwoCard(Card):
    def __init__(self, color):
        self.color = color

    def actions(self, lastCard, indexPlayer, players, deck):

        if lastCard.color not in [self.color, None]:
            raise Exception("Not same color")

        # make next player buy two cards
        for i in range(2):
            players[indexPlayer + 1].addCard(deck.pickCard())

        return indexPlayer


class InvertedCard(Card):
    def __init__(self, color):
        self.color = color

    def actions(self, lastCard, indexPlayer, players, deck):

        if lastCard.color not in [self.color, None
                                  ] and not isinstance(lastCard, InvertedCard):
            raise Exception("Not same color or card type")

        # reverse list and set correct index
        playerId = players[indexPlayer].id
        players.reverse()

        for i in range(len(players)):
            if players[i].id == playerId:
                indexPlayer = i
                break

        return indexPlayer


class JumpCard(Card):
    def __init__(self, color):
        self.color = color

    def actions(self, lastCard, indexPlayer, players, deck):

        if lastCard.color not in [self.color, None]:
            raise Exception("Not same color")

        # jump player
        if indexPlayer == len(players) - 1:
            indexPlayer = 0
        else:
            indexPlayer += 1

        return indexPlayer


class JokerCard(Card):
    def __init__(self):
        self.color = False

    def setColor(self, color: str):
        self.color = color

    def actions(self, lastCard, indexPlayer, players, deck):
        return indexPlayer


class JokerPlusFourCard(Card):
    def __init__(self):
        pass

    def setColor(self, color: str):
        self.color = color

    def actions(self, lastCard, indexPlayer, players, deck):
        # make next player buy two cards
        for i in range(4):
            players[indexPlayer + 1].addCard(deck.pickCard())
        return indexPlayer
