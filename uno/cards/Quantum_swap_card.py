from cards.card import Card
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class Quantum_swap_card(Card):
    """A card that swaps cards of two players using a quantum CSWAP gate, measuring only the data qubits."""
    def __init__(self, color, max_cards=8):
        super().__init__(color, "Quantum Hand Swap")
        self.cardId = 16

    def play(self, game):
        self.activate_quantum_effect(game, game.get_current_player(), game.get_next_player())

    def activate_quantum_effect(self, game, player1, player2):
        n1, n2 = len(player1.Hand), len(player2.Hand)
        n_swap = min(n1, n2)

        if n_swap == 0:
            return  # Nothing to swap

        # total qubits = 1 (control) + 2 * n_swap (cards)
        total_qubits = 1 + 2 * n_swap
        qc = QuantumCircuit(total_qubits, 2 * n_swap)  # Only measure data qubits

        # Control in superposition
        qc.h(0)

        # Apply CSWAPs: control is qubit 0, pairs are (1+i, 1+n_swap+i)
        for i in range(n_swap):
            qc.cswap(0, 1 + i, 1 + n_swap + i)

        # Measure only the card qubits, skipping the control (qubit 0)
        for i in range(2 * n_swap):
            qc.measure(1 + i, i)

        # Run on simulator
        backend = AerSimulator()
        qc = transpile(qc, backend)
        result = backend.run(qc, shots=1).result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0][::-1]  # Reverse to align with qubit index

        print(f"[Quantum SWAP] Measured bitstring: {bitstring}")

        # Decode result into new hands
        new_hand1 = []
        new_hand2 = []

        for i in range(n_swap):
            # Index in bitstring:
            # - player1 data qubits are first half [0:n_swap]
            # - player2 data qubits are second half [n_swap:2*n_swap]
            b1 = bitstring[i]
            b2 = bitstring[n_swap + i]

            if b1 == '1':
                new_hand1.append(player1.Hand[i])
            else:
                new_hand2.append(player1.Hand[i])

            if b2 == '1':
                new_hand1.append(player2.Hand[i])
            else:
                new_hand2.append(player2.Hand[i])

        # Add remaining cards if any (those that weren't swapped)
        new_hand1.extend(player1.Hand[n_swap:])
        new_hand2.extend(player2.Hand[n_swap:])

        # Apply hands
        player1.Hand = new_hand1
        player2.Hand = new_hand2

        print(f"[Quantum SWAP] {player1.GetName()} new hand: {[str(c) for c in player1.Hand]}")
        print(f"[Quantum SWAP] {player2.GetName()} new hand: {[str(c) for c in player2.Hand]}")
