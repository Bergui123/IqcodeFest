# quantum_card.py
# Exemple of a quantum card that uses Qiskit to create a quantum effect #
import sys
import os
sys.path.append(os.path.dirname(__file__)) 
from card import Card
from qiskit import QuantumCircuit

class QuantumCard(Card):
    def __init__(self, color, value):
        super().__init__(color, value)
        self.circuit = self.create_circuit()
    
    def create_circuit(self):
        qc = QuantumCircuit(1)
        qc.h(0)  # Put qubit in superposition
        qc.measure_all()
        return qc
    
    def run_quantum_effect(self):
        # backend = Aer.get_backend('aer_simulator')
        # job = execute(self.circuit, backend, shots=1)
        # result = job.result()
        # counts = result.get_counts()
        return 0
    
    def play(self, game):
        super().play(game)
        counts = self.run_quantum_effect()
        # Example effect: if measured '0', skip next player; else reverse
        if '0' in counts:
            game.skip_next_player = True
            game.ui.set_info("QuantumCard effect: Skipping next player!")
        else:
            game.reverse_turn_order()
            game.ui.set_info("QuantumCard effect: Reversing turn order!")
