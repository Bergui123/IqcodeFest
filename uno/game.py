from deck import create_deck
from player_module import Player

class UnoGame:
    def __init__(self, ui):
        self.ui = ui
        self.deck = create_deck()
        self.discard_pile = []
        
        # Create 4 players: 1 human, 3 computers
        self.players = [
            Player("You"),
            Player("Computer 1"),
            Player("Computer 2"),
            Player("Computer 3"),
        ]
        
        # Deal 7 cards to each player
        for _ in range(7):
            for player in self.players:
                player.draw_card(self.deck)
        
        self.discard_pile.append(self.deck.pop())
        
        self.current_player_idx = 0
        self.turn_direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.skip_next = False
    
    def get_current_player(self):
        return self.players[self.current_player_idx]
    
    def reverse_turn_order(self):
        self.turn_direction *= -1
    
    def get_top_card(self):
        return self.discard_pile[-1]
    
    def can_play(self, card):
        return card.matches(self.get_top_card())
    
    def play_card(self, player, card_index):
        card = player.hand[card_index]
        if self.can_play(card):
            # Remove card from player's hand
            player.hand.pop(card_index)
            # Place card on discard pile
            self.discard_pile.append(card)
            # Trigger card effect
            card.play(self)
            self.ui.update()
            return True
        return False
    
    def draw_card(self, player):
        card = player.draw_card(self.deck)
        self.ui.update()
        return card
    
    def advance_turn(self):
        # Handle skip effect
        if self.skip_next:
            self.skip_next = False
            # Skip the next player by moving an extra step
            self.current_player_idx = (self.current_player_idx + self.turn_direction) % len(self.players)
        
        # Advance to next player
        self.current_player_idx = (self.current_player_idx + self.turn_direction) % len(self.players)
        
        # If current player has no cards, game should end before next action
    
    def next_player(self):
        return self.players[self.current_player_idx + self.turn_direction]
    
    def check_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player.name
        return None
