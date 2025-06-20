import random
from uno.cards.card import Card
from uno.cards.Quantum_color_card       import Quantum_color_card
from uno.cards.quantum_balance_card import quantum_balance_card
from uno.cards.quantum_card import quantum_card
from uno.cards.Quantum_draw_card       import Quantum_draw_card
from uno.cards.Quantum_grover_card import Quantum_grover_card
from uno.cards.Quantum_shuffle_card    import Quantum_shuffle_card
from uno.cards.Quantum_swap_card      import Quantum_swap_card
from uno.cards.teleportation_card import teleportation_card
def create_card_by_id(card_id):
    """Return an instance of a card based on its ID."""

    colors = ["Red", "Green", "Blue", "Yellow"]

    # Importer localement ici pour éviter les circular imports
    if card_id == 15:
        from uno.cards.Quantum_superposed_card import Quantum_superposed_card
        return Quantum_superposed_card(random.choice(colors), 8)

    card_map = {
        0: Card(random.choice(colors), 0),
        1: Card(random.choice(colors), 1),
        2: Card(random.choice(colors), 2),
        3: Card(random.choice(colors), 3),
        4: Card(random.choice(colors), 4),
        5: Card(random.choice(colors), 5),
        6: Card(random.choice(colors), 6),
        7: Card(random.choice(colors), 7),
        8: Card(random.choice(colors), 8),
        9: Card(random.choice(colors), 9),
        10: quantum_balance_card(random.choice(colors)),
        11: quantum_card(random.choice(colors)),
        12: Quantum_color_card(colors, random.choice(colors)),
        13: Quantum_draw_card(random.choice(colors), 8),
        14: Quantum_shuffle_card(random.choice(colors)),
        16: Quantum_swap_card(random.choice(colors)),
        17: Quantum_grover_card(random.choice(colors)),
        18: teleportation_card(random.choice(colors)),
    }

    return card_map.get(card_id, None)
