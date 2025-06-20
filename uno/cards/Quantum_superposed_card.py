from cards.card import Card
from cards.utils.card_factory import create_card_by_id
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class Quantum_superposed_card(Card):
    """A card that creates a superposition over all possible card IDs and adds one to the next player."""
    def __init__(self, color, max_card_id=18):
        super().__init__(color, "Quantum Superposed Card")
        self.max_card_id = max_card_id
        self.cardId = 15

    def play(self, game):
        """Generate a card ID via quantum effect and add the corresponding card to the next player's hand."""
        card_id = self.activate_quantum_effect()

        # Créer la carte correspondante
        card = create_card_by_id(card_id)

        if card:
            print(f"[Quantum Superposed Card] Added card with ID {card_id} to next player.")
            game.get_next_player().Hand.append(card)
        else:
            print(f"[Quantum Superposed Card] Invalid card ID generated: {card_id}")

    def activate_quantum_effect(self):
        """Quantum generation of an integer between 0 and max_card_id inclusive."""
        n_qubits = 5  # 2^5 = 32 > max_card_id
        qc = QuantumCircuit(n_qubits, n_qubits)

        for q in range(n_qubits):
            qc.h(q)

        qc.measure(range(n_qubits), range(n_qubits))

        sim = AerSimulator()
        qc = transpile(qc, sim)
        result = sim.run(qc, shots=1).result()
        counts = result.get_counts()

        bitstring = list(counts.keys())[0]
        number = int(bitstring, 2) % (self.max_card_id + 1)

        print(f"[Quantum Superposed Card] Measured bitstring: {bitstring} -> cardId {number}")

        return number
