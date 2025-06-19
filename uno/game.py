# game.py
from deck import create_deck
from player_module import Player

class UnoGame:
    def __init__(self, ui):
        self.ui = ui
        self.deck = create_deck()
        self.discard_pile = []
        
        self.player = Player("You")
        self.computer = Player("Computer")
        
        for _ in range(7):
            self.player.draw_card(self.deck)
            self.computer.draw_card(self.deck)
        
        self.discard_pile.append(self.deck.pop())
        
        self.player_turn = True
        self.skip_next_player = False
        self.turn_direction = 1  # 1 for normal, -1 for reversed
    
    def reverse_turn_order(self):
        self.turn_direction *= -1
    
    def get_top_card(self):
        return self.discard_pile[-1]
    
    def can_play(self, card):
        return card.matches(self.get_top_card())
    
    def play_card(self, player, card_index):
        card = player.hand[card_index]
        if self.can_play(card):
            card.play(self)
            player.hand.pop(card_index)
            self.ui.update()
            return True
        return False
    
    def draw_card(self, player):
        card = player.draw_card(self.deck)
        self.ui.update()
        return card
    
    def next_turn(self):
        if self.skip_next_player:
            self.skip_next_player = False
            self.player_turn = not self.player_turn  # skip turn
        
        else:
            self.player_turn = not self.player_turn
    
    def check_winner(self):
        if len(self.player.hand) == 0:
            return self.player.name
        if len(self.computer.hand) == 0:
            return self.computer.name
        return None
