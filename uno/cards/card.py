# cards.py
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.cardId = None

    def __str__(self):
        return f"{self.color} {self.value}"

    def matches(self, other):
        return self.color == other.color or self.value == other.value or other.color == "Quantum" or self.color == "Quantum"

    def play(self, game):
        # Default card: no special effect, just advance turn
        game.discard_pile.append(self)