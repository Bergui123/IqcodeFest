import random
from cards.card import Card
from cards.utils.grover_utils import grover_card_search, card_to_index
from qiskit_aer import AerSimulator


class Quantum_grover_card(Card):
    def __init__(self, color="Purple"):
        super().__init__(color, "Quantum Grover")
        self.cardId = 17  # Just an arbitrary ID
        self.selected_card = None 

    def play(self, game, selected_card=None):
        current_player = game.get_current_player()
        other_players = [p for p in game.players if p != current_player]

        if self.selected_card is None:
            # Appel initial : l'UI doit déclencher la sélection
            print(current_player.is_bot())
            if not current_player.is_bot():
                return "UI_SELECT"
            else:
                # Bot pick
                choice = random.randrange(len(current_player.GetHand()))
                self.selected_card = current_player.GetHand()[choice]

        print(f"\n🔍 Grover scan for: {self.selected_card}\n")

        for player in other_players:
            Hand = player.GetHand()
            found = grover_card_search(Hand, self.selected_card, verbose=False)
            if found:
                index = card_to_index(self.selected_card, Hand)
                print(f"✅ {player.GetName()} has {self.selected_card} at index {index}. Adding {index} card(s) as penalty.")
                for _ in range(index):
                    new_card = game.draw_card(game.players.index(player))
                    if new_card:
                        player.AddCard(new_card)
            else:
                print(f"❌ {player.GetName()} does not have {self.selected_card}.")

        game.discard_pile.append(self)
        game.next_turn()
