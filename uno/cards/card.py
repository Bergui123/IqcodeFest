# cards.py
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    
    def __str__(self):
        return f"{self.color} {self.value}"
    
    def matches(self, other):
        return self.color == other.color or self.value == other.value
    
    def play(self, game):
        # Default effect: just put card on discard pile
        game.discard_pile.append(self)
