# quantum_card.py
# Exemple of a quantum card that uses Qiskit to create a quantum effect #
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from cards.card import Card

class quantum_card(Card):
    def __init__(self, color):
        super().__init__(color, "Quantum Effect Card")
        self.circuit = self.create_circuit()
        self.cardId = 11  # Unique identifier for this card type
    
    def create_circuit(self):
        qc = QuantumCircuit(1)
        qc.h(0)  # Put qubit in superposition
        qc.measure_all()
        return qc
    
    def run_quantum_effect(self):
        backend = AerSimulator()
        qc = self.create_circuit()
        transpiled = transpile(qc, backend=backend)
        result = backend.run(transpiled, shots=1).result()
        counts = result.get_counts()
        return counts
    
    def play(self, game):
        super().play(game)
        counts = self.run_quantum_effect()
        # Example effect: if measured '0', skip next player; else reverse
        if '0' in counts:
            game.skip_next_player = True
            
        else:
            game.reverse_turn_order()
        
