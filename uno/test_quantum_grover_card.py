from uno.cards.Quantum_grover_card import QuantumGroverCard
from cards.card import Card
from QuantumCode.Player import Player
from uno.QuantumCode.GameController import Game

def create_sample_card(color, value):
    return Card(color, value)

def main():
    # Create the game and add players
    game = Game()
    game.add_player("Alice")
    game.add_player("Bob")
    game.add_player("Charlie")
    game.current_player_idx = 0  # Alice's turn

    # Clear any existing cards in hands (prudent)
    for player in game.players:
        player.GetHand().clear()

    # Add cards manually using AddCard()
    game.players[0].AddCard(create_sample_card("Blue", "Draw Two"))  # Alice
    game.players[0].AddCard(create_sample_card("Green", 4))

    game.players[1].AddCard(create_sample_card("Red", 5))            # Bob
    game.players[1].AddCard(create_sample_card("Blue", "Draw Two"))  # match!
    game.players[1].AddCard(create_sample_card("Yellow", 1))

    game.players[2].AddCard(create_sample_card("Green", 9))          # Charlie
    game.players[2].AddCard(create_sample_card("Red", 3))

    # Add some cards to the deck to allow penalty draws
    game.deck.CardInPile = [
        create_sample_card("Red", 9),
        create_sample_card("Yellow", 0),
        create_sample_card("Green", 2),
        create_sample_card("Blue", 1),
    ]

    print("\n===== Before playing Quantum Grover =====")
    for p in game.players:
        print(f"{p.GetName()} hand: {[str(c) for c in p.GetHand()]}")

    # Example: add and play Quantum Grover card if you want
    quantum_card = QuantumGroverCard()
    game.players[0].AddCard(quantum_card)
    game.play_card(0,2)

    print("\n===== After playing Quantum Grover =====")
    for p in game.players:
        print(f"{p.GetName()} hand: {[str(c) for c in p.GetHand()]}")

if __name__ == "__main__":
    main()
