from cards.card import Card
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile

class QuantumSuperposedCard(Card):
    """A card superposed and is only measured when played."""
    def __init__(self, color, max_cards=8):
        super().__init__(color, f"Quantum Superposed up to {max_cards}")
        self.max_cards = max_cards
        self.cardId=15
        self.number_of_different_cards = 19  # Maximum number of different cards to draw

    def play(self, game):
        """Play the quantum superposed card effect."""
        game.ui.set_info(f"{self.color} Quantum Superposed Card played! Activating quantum effect...")
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
        """Generate a quantum random number between 0 and number of different cards (inclusive)."""
        n_qubits = 5  # Enough to represent numbers up to 31 (2^5 - 1)
        # Create a quantum circuit with n_qubits qubits and n_qubits classical bits
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
        number = int(bitstring, 2)% (self.number_of_different_cards+1)

        
        # Rejection sampling if number > max_cards
        return number