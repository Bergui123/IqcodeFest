from cards.quantum_balance_card import QuantumBalanceCard
from QuantumCode.Player import Player
from cards.card import Card

class DummyUI:
    def set_info(self, msg):
        print(f"UI info: {msg}")


class DummyGame:
    def __init__(self):
        self.players = [Player("Alice"), Player("Bob")]
        self.current_player_idx = 0
        self.ui = DummyUI()  # ou une version mock
        # Ajoute des cartes fictives aux joueurs si nécessaire

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def get_next_player(self):
        return self.players[(self.current_player_idx + 1) % len(self.players)]

def create_sample_card(color, value):
    # Simplified card for test
    return Card(color, value)

def main():
    game = DummyGame()

   # Give player 1 some cards (initially 10 cards)
    game.players[0].Hand = [
        create_sample_card('Red', 1),
        create_sample_card('Green', 3),
        create_sample_card('Blue', 5),
        create_sample_card('Yellow', 'Skip'),
        create_sample_card('Red', 'Reverse'),
        create_sample_card('Green', 7),
        create_sample_card('Blue', 9),
        create_sample_card('Yellow', 2),
        create_sample_card('Red', 'Draw Two'),
        create_sample_card('Green', 1)
    ]

    # Give player 2 some cards (initially 10 cards)
    game.players[1].Hand = [
        create_sample_card('Red', 2),
        create_sample_card('Green', 4),
        create_sample_card('Blue', 'Draw Two'),
        create_sample_card('Yellow', 6),
        create_sample_card('Red', 'Skip'),
        create_sample_card('Green', 5),
        create_sample_card('Blue', 8),
        create_sample_card('Yellow', 1),
        create_sample_card('Red', 3),
        create_sample_card('Green', 2)
    ]


    print("Before balancing:")
    for i, p in enumerate(game.players):
        print(f"Player {i+1} Hand: {[str(card) for card in p.Hand]}")

    # Create and play QuantumBalanceCard
    qb_card = QuantumBalanceCard()
    qb_card.play(game)

    print("\nAfter balancing:")
    for i, p in enumerate(game.players):
        print(f"Player {i+1} Hand: {[str(card) for card in p.Hand]}")

if __name__ == "__main__":
    main()

    
