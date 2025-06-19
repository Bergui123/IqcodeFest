# Add project root to module search path
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
from uno.QuantumCode.Deck import Deck
from uno.QuantumCode.Player import Player
from uno.cards.card import Card

class GameLogic:
    def __init__(self):
        self.deck = Deck()
        self.discard_pile = []
        self.players = []
        self.current_player_idx = 0

    def add_players(self):
        while True:
            try:
                num = int(input("Enter number of players (2-10): "))
                if 2 <= num <= 10:
                    break
                print("Please enter a number between 2 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        for i in range(num):
            name = input(f"Enter name for player {i+1}: ")
            self.players.append(Player(name))

    def build_deck(self):
        colors = ["Red", "Green", "Blue", "Yellow"]
        values = [str(n) for n in range(0, 10)]
        # Add number cards: zero once, 1-9 twice per color
        for color in colors:
            self.deck.CardInPile.append(Card(color, "0"))
            for v in values[1:]:
                self.deck.CardInPile.append(Card(color, v))
                self.deck.CardInPile.append(Card(color, v))
        random.shuffle(self.deck.CardInPile)

    def deal(self):
        # Deal 7 cards to each player
        for _ in range(7):
            for p in self.players:
                if self.deck.CardInPile:
                    p.AddCard(self.deck.CardInPile.pop(0))

    def start(self):
        self.add_players()
        self.build_deck()
        self.deal()
        # Flip first card to start discard pile
        if self.deck.CardInPile:
            first = self.deck.CardInPile.pop(0)
            self.discard_pile.append(first)
            print(f"Starting card: {first}")
        self.game_loop()

    def game_loop(self):
        while True:
            player = self.players[self.current_player_idx]
            top = self.discard_pile[-1]
            print(f"\n{player.GetName()}'s turn. Top card: {top}")
            hand = player.GetHand()
            # Display hand
            for idx, card in enumerate(hand):
                print(f"  {idx}: {card}")
            choice = input("Choose card index to play or 'd' to draw: ")
            if choice.lower() == 'd':
                # Draw a card
                if self.deck.CardInPile:
                    drawn = self.deck.CardInPile.pop(0)
                    player.AddCard(drawn)
                    print(f"{player.GetName()} draws {drawn}")
                else:
                    print("Deck is empty!")
            else:
                try:
                    idx = int(choice)
                    card = hand[idx]
                    if card.matches(top):
                        played = player.PlayCard(idx)
                        self.discard_pile.append(played)
                        print(f"{player.GetName()} plays {played}")
                        if not player.GetHand():
                            print(f"{player.GetName()} wins!")
                            break
                    else:
                        print("Card does not match top card. Try again.")
                        continue
                except (ValueError, IndexError):
                    print("Invalid choice. Try again.")
                    continue
            # Next player's turn
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        print("Game over.")

if __name__ == "__main__":
    GameLogic().start()