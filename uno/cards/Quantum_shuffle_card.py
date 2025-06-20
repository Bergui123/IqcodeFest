from cards.card import Card
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile

class Quantum_shuffle_card(Card):
    """A card that shuffles the cards in all the player's hands using quantum principles."""
    def __init__(self, color, max_cards=8):
        super().__init__(color, f"Quantum Shuffle up to {max_cards}")
        self.max_cards = max_cards
        self.cardId = 14  # Unique identifier for this card type

    def play(self, game):
        """Play the quantum shuffle card effect."""
        self.activate_quantum_effect(game)

    def activate_quantum_effect(self, game):
        """Shuffle the hands of all players using quantum principles."""
        n_players = len(game.players)
        max_cards_hands = max(len(player.Hand) for player in game.players) 
        n_qubits = n_players * max_cards_hands  # Enough qubits to represent all cards in hands
        cards = []
        for player in game.players:
            cards.append(player.Hand)

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
        
        for player in game.players:
            new_hand = []
            for i in range(max_cards_hands):         
                if len(cards) == 0:
                    continue       
                new_hand.append(cards.pop(number % len(cards)))
            player.Hand = new_hand        
