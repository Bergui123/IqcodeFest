# player.py

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def draw_card(self, deck):
        if deck:
            card = deck.pop()
            self.hand.append(card)
            return card
        return None
    
    def play_card(self, index):
        return self.hand.pop(index)
