from cards.card import Card
from cards.Quantum_color_card import QuantumColorCard  # adjust if the file is in the same directory

# --- Mocks ---
class MockUI:
    def set_info(self, msg):
        print("[UI]", msg)

class MockGame:
    def __init__(self):
        self.colors = ["Red", "Blue", "Green", "Yellow"]
        self.current_color = "Blue"
        self.ui = MockUI()

    def get_top_card(self):
        return Card("Blue", 5)

# --- Test Function ---
def test_quantum_color_card():
    game = MockGame()
    q_card = QuantumColorCard(color_list=game.colors, current_color=game.current_color)

    print("\n===== Before playing QuantumColorCard =====")
    print(f"Current color: {game.current_color}")

    q_card.play(game)

    print("\n===== After playing QuantumColorCard =====")
    print(f"New color: {game.current_color}")
    assert game.current_color in game.colors, "New color should be a valid color"

# --- Run the test ---
if __name__ == "__main__":
    test_quantum_color_card()
