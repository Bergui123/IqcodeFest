from cards.card import Card
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class Quantum_swap_card(Card):
    """A card that swaps cards of two players using a quantum CSWAP gate, measuring the control and data qubits."""
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
        # Measure all qubits including control qubit
        qc = QuantumCircuit(total_qubits, total_qubits)

        # Control in superposition
        qc.h(0)

        # Apply CSWAP gates controlled by qubit 0
        for i in range(n_swap):
            qc.cswap(0, 1 + i, 1 + n_swap + i)

        # Measure all qubits
        qc.measure(range(total_qubits), range(total_qubits))

        # Run on simulator
        backend = AerSimulator()
        qc = transpile(qc, backend)
        result = backend.run(qc, shots=1).result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0][::-1]  # Reverse to align qubit index with bitstring index

        print(f"[Quantum SWAP] Measured bitstring: {bitstring}")

        control_bit = bitstring[0]

        new_hand1 = []
        new_hand2 = []

        if control_bit == '1':
            # Swap first n_swap cards
            for i in range(n_swap):
                new_hand1.append(player2.Hand[i])
                new_hand2.append(player1.Hand[i])
        else:
            # Keep hands as is for first n_swap cards
            for i in range(n_swap):
                new_hand1.append(player1.Hand[i])
                new_hand2.append(player2.Hand[i])

        # Append remaining cards (those beyond n_swap)
        new_hand1.extend(player1.Hand[n_swap:])
        new_hand2.extend(player2.Hand[n_swap:])

        # Apply new hands
        player1.Hand = new_hand1
        player2.Hand = new_hand2

        print(f"[Quantum SWAP] {player1.GetName()} new hand: {[str(c) for c in player1.Hand]}")
        print(f"[Quantum SWAP] {player2.GetName()} new hand: {[str(c) for c in player2.Hand]}")
