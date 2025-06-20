# Add project root to module search path
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from uno.QuantumCode.GameController import Game
from uno.cards.card import Card
from uno.QuantumCode.Player import Player
from uno.Bot.BotCode import BotCode

class GameLogic:
    def __init__(self):
        self.controller = Game()

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
            self.controller.add_player(name)
        # Add a bot that always draws
        bot = BotCode()
        self.controller.players.append(bot)
        print(f"Added bot: {bot.GetName()}")

    def start(self):
        self.add_players()
        self.controller.start()
        first = self.controller.get_top_card()
        print(f"Starting card: {first}")
        self.game_loop()

    def game_loop(self):
        while True:
            player = self.controller.get_current_player()
            if hasattr(player, 'is_bot') and player.is_bot:
                drawn = player.take_turn(self.controller)
                if drawn:
                    print(f"{player.GetName()} draws {drawn}")
                else:
                    print(f"{player.GetName()} tried to draw but deck is empty!")
                self.controller.next_turn()
                continue
            top = self.controller.get_top_card()
            print(f"\n{player.GetName()}'s turn. Top card: {top}")
            Hand = player.GetHand()
            # Display Hand
            for idx, card in enumerate(Hand):
                print(f"  {idx}: {card}")
            choice = input("Choose card index to play or 'd' to draw: ")
            if choice.lower() == 'd':
                drawn = self.controller.draw_card(self.controller.current_player_idx)
                if drawn:
                    print(f"{player.GetName()} draws {drawn}")
                else:
                    print("Deck is empty!")
            else:
                try:
                    idx = int(choice)
                    card = Hand[idx]
                    if card.matches(top):
                        played = self.controller.play_card(self.controller.current_player_idx, idx)
                        print(f"{player.GetName()} plays {played}")
                        winner = self.controller.has_winner()
                        if winner:
                            print(f"{winner.GetName()} wins!")
                            break
                    else:
                        print("Card does not match top card. Try again.")
                        continue
                except (ValueError, IndexError):
                    print("Invalid choice. Try again.")
                    continue
            # Next player's turn
            self.controller.next_turn()
        print("Game over.")

if __name__ == "__main__":
    GameLogic().start()