from cards.quantum_card import QuantumCard

# Mock UI class to simulate game UI
class MockUI:
    def set_info(self, msg):
        print(f"[UI] {msg}")

# Mock Game class to test QuantumCard
class MockGame:
    def __init__(self):
        self.skip_next_player = False
        self.reversed = False
        self.ui = MockUI()
        self.discard_pile = []  # <-- ajoute ceci pour éviter l'erreur

    def reverse_turn_order(self):
        self.reversed = True
        print("[Game] Turn order reversed.")

    def get_state(self):
        return {
            "skip_next_player": self.skip_next_player,
            "reversed": self.reversed,
            "discard_pile_size": len(self.discard_pile)
        }

def main():
    # Create a QuantumCard
    qc = QuantumCard("Purple", "Quantum Flip")

    # Create a mock game object
    game = MockGame()

    # Play the card
    qc.play(game)

    # Show game state
    print("Game state after playing QuantumCard:", game.get_state())

if __name__ == "__main__":
    main()
