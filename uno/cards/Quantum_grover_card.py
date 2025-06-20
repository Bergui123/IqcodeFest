from cards.card import Card
from cards.utils.grover_utils import grover_card_search, card_to_index
from qiskit_aer import AerSimulator


class Quantum_grover_card(Card):
    def __init__(self, color="Purple"):
        super().__init__(color, "Quantum Grover")
        self.cardId = 42  # Just an arbitrary ID

    def play(self, game):
        current_player = game.get_current_player()
        current_hand = current_player.GetHand()
        other_players = [p for p in game.players if p != current_player]

        # Ask the player to choose a card from their hand
        print(f"\n🔮 {current_player.GetName()} played Quantum Grover!")
        print("Select a card from your hand to search in opponents' hands:")
        for i, card in enumerate(current_hand):
            print(f"  {i}: {card}")

        while True:
            try:
                choice = int(input("Enter the index of the card to scan for: "))
                target_card = current_hand[choice]
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid card index.")


        print(f"\nRunning Grover’s algorithm for: {target_card}\n")

        for player in other_players:
            hand = player.GetHand()
            found = grover_card_search(hand, target_card, verbose=False)
            if found:
                index = card_to_index(target_card, hand)
                print(f"✅ {player.GetName()} has {target_card} at index {index}. Adding {index} card(s) as penalty.")
                for _ in range(index):
                    new_card = game.draw_card(game.players.index(player))
                    if new_card:
                        player.AddCard(new_card)
            else:
                print(f"❌ {player.GetName()} does not have {target_card}.")

        # Discard this card
        game.discard_pile.append(self)
        game.next_turn()
