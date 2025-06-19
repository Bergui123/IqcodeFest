# quantum_draw_card.py
from cards.card import Card
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile

class QuantumDrawCard(Card):
    def __init__(self, color, max_cards=8):
        super().__init__(color, f"Quantum Draw up to {max_cards}")
        self.max_cards = max_cards
        self.cardId = 13  # Unique identifier for this card type

    def play(self, game):
        """Play the quantum draw card effect."""
        game.ui.set_info(f"{self.color} Quantum Draw Card played! Activating quantum effect...")
        drawn_cards = self.activate_quantum_effect()
        game.ui.set_info(f"Drawn {drawn_cards} cards from the deck.")
        
        for _ in range(drawn_cards):
            card = game.deck.draw_card()
            if card:
                game.next_player.hand.append(card)
                game.ui.set_info(f"{game.current_player.name} drew a card: {card}")
            else:
                game.ui.set_info("No more cards in the deck to draw.")

    def activate_quantum_effect(self):
        """Generate a quantum random number between 0 and max_cards (inclusive)."""
        n_qubits = 3  #
        qc = QuantumCircuit(n_qubits, n_qubits)

        # Put all qubits into superposition
        for q in range(n_qubits):
            qc.h(q)

        qc.measure(range(n_qubits), range(n_qubits))
        sim = AerSimulator()    
        qc = transpile(qc, sim)
        job = sim.run(qc)
        result = job.result()
        counts = result.get_counts()

        bitstring = list(counts.keys())[0]
        number = int(bitstring, 2)
        print(f"Measured number: {number}")

        # Rejection sampling if number > max_cards
        if number > self.max_cards:
            return self.activate_quantum_effect()
        else:
            return number
