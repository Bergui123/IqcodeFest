from cards.card import Card
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

class QuantumColorCard(Card):
    """
    Uses a full 1D discrete-time coined quantum walk to choose a color.
    """

    def __init__(self, color_list, current_color="Red"):
        self.colors = color_list
        self.current_color = current_color
        self.cardId = 12
        super().__init__("Quantum", "Color")

    def play(self, game):
        game.ui.set_info(f"{self.color} Quantum Color Card played! Activating quantum walk...")
        new_color = self.activate_quantum_walk()
        game.ui.set_info(f"Color changed to {new_color}.")
        game.current_color = new_color

    def activate_quantum_walk(self, steps=np.random.randint(1, 5)):
        """
        Perform a 1D discrete-time quantum walk with 3 steps on 4 colors.
        Position: 2 qubits (q0 = LSB, q1 = MSB), Coin: 1 qubit (q2)
        """
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator

        color_map = {
            0: "Red",
            1: "Blue",
            2: "Green",
            3: "Yellow",
        }

        qc = QuantumCircuit(3, 2)  # q0, q1 = position; q2 = coin

        # Initialize walker to current position
        pos_index = self.colors.index(self.current_color)
        if pos_index & 0b01:
            qc.x(0)  # LSB
        if pos_index & 0b10:
            qc.x(1)  # MSB

        # Initialize coin qubit in |+⟩
        qc.h(2)

        for _ in range(steps):
            # Step 1: Coin toss (Hadamard on coin qubit)
            qc.h(2)

            # Step 2: Shift operator — controlled shift depending on coin
            # If coin == |0>: move left (decrement mod 4)
            # If coin == |1>: move right (increment mod 4)

            # Right shift (|i+1 mod 4⟩): controlled by coin in state |1⟩
            qc.x(2)
            self._increment_mod_4(qc, control=2, q0=0, q1=1)
            qc.x(2)

            # Left shift (|i-1 mod 4⟩): controlled by coin in state |0⟩
            self._decrement_mod_4(qc, control=2, q0=0, q1=1)

        # Measure position qubits
        qc.measure(0, 0)
        qc.measure(1, 1)

        # Run on simulator
        backend = AerSimulator()
        transpiled = transpile(qc, backend)
        result = backend.run(transpiled, shots=1).result()
        counts = result.get_counts()
        measured = list(counts.keys())[0]
        pos = int(measured[::-1], 2)  # fix Qiskit's endianness

        return color_map[pos]

    def _increment_mod_4(self, qc, control, q0, q1):
        """Controlled increment modulo 4 on 2 position qubits"""
        # q0 is LSB, q1 is MSB
        qc.cx(control, q0)
        qc.ccx(control, q0, q1)

    def _decrement_mod_4(self, qc, control, q0, q1):
        """Controlled decrement modulo 4 on 2 position qubits"""
        # Implemented as controlled subtract 1 mod 4
        # Truth table (q0, q1):
        # 00 -> 11
        # 01 -> 00
        # 10 -> 01
        # 11 -> 10

        # Inverse of increment
        qc.ccx(control, q0, q1)
        qc.cx(control, q0)
