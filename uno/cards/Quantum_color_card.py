from cards.card import Card
from qiskit import QuantumCircuit
from qiskit.circuit.library import PermutationGate
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile

class QuantumColorCard(Card):
    "Changes the color of the game using quantum walker principles between a graph where each node is a colour."

    def __init__(self, game):
        self.colors = game.colors
        self.current_color = game.get_top_card().color if game.get_top_card() else "Red"  # Default to Red if no top card
        self.cardId = 21  # Unique identifier for this card type
        super().__init__(game, self.cardId)

    def play(self, game):
        """Play the quantum color card effect."""
        game.ui.set_info(f"{self.color} Quantum Color Card played! Activating quantum effect...")
        new_color = self.activate_quantum_effect()
        game.ui.set_info(f"Color changed to {new_color}.")
        game.current_color = new_color

    def activate_quantum_effect(self):
        """create a graph with colors as nodes and apply a quantum walk to change the color."""
        n_qubits =len(self.colors)/2 +1# number of colors
        n_steps = 6
        # create a quantum circuit with n_qubits qubits
        circuit = QuantumCircuit(n_qubits, name="Quantum Color Circuit")
        # create a circuit with colors as nodes
        # Initialize the position register with the current color index
        color_index = self.colors.index(self.current_color)
        if color_index== 1:
            circuit.x(1)  # If the current color is Blue, flip the second qubit
        elif color_index == 2:
            circuit.x(0)
        elif color_index == 3:
            circuit.x(0,1)  # If the current color is Yellow, flip the first two qubits
        circuit.h(2)
        # Pre-build shift unitaries on the position register
        shift_plus  = PermutationGate([1, 2, 3, 0], label="S₊").to_instruction()
        shift_minus = PermutationGate([3, 0, 1, 2], label="S₋").to_instruction()
        for _ in range(n_steps):
            circuit.h(2)
            circuit.append(shift_plus.control(1), [2, 0, 1])
            # (c) If coin = |0⟩ do –1 mod 4
            circuit.x(2)
            circuit.append(shift_minus.control(1), [2, 0, 1])
            circuit.x(2)
        circuit.measure([0,1], [0,1])
        sim = AerSimulator()
        qc = transpile(circuit, sim)
        job = sim.run(qc)
        result = job.result()
        counts = result.get_counts()  # Measure the qubits to get the color index
        if counts.item(0,1) == 00:
            return self.colors[0]# If the result is 00, change the color to Red
        elif counts.item(0,1) == 01:
            return self.colors[1]
        elif counts.item(0,1) == 10:
            return self.colors[2]
        elif counts.item(0,1) == 11:
            return self.colors[3]
