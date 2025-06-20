from cards.card import Card
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import math

class Quantum_shuffle_card(Card):
    """A card that shuffles all cards from all players using quantum-generated indices."""
    def __init__(self, color):
        super().__init__(color, "Quantum True Shuffle")
        self.cardId = 14

    def play(self, game):
        self.quantum_shuffle(game)

    def quantum_shuffle(self, game):
        # Collect all cards from players
        full_deck = []
        for player in game.players:
            full_deck.extend(player.Hand)
            player.Hand.clear()

        num_players = len(game.players)
        player_index = 0

        while len(full_deck) > 0:
            # Determine number of qubits required to index current deck
            num_qubits = math.ceil(math.log2(len(full_deck)))
            if num_qubits == 0:
                idx = 0
            else:
                idx = self.quantum_random_index(num_qubits) % len(full_deck)

            # Remove the card at the selected index and assign it to a player
            selected_card = full_deck.pop(idx)
            game.players[player_index].Hand.append(selected_card)

            player_index = (player_index + 1) % num_players

    def quantum_random_index(self, n_qubits):
        """Generates a quantum random integer using n_qubits."""
        qc = QuantumCircuit(n_qubits, n_qubits)
        qc.h(range(n_qubits))
        qc.measure(range(n_qubits), range(n_qubits))

        sim = AerSimulator()
        transpiled = transpile(qc, sim)
        result = sim.run(transpiled, shots=1).result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0]
        return int(bitstring, 2)
