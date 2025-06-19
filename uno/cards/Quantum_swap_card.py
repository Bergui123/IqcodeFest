from cards.card import Card
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile

class QuantumSwapCard(Card):
    """A card that swaps the hands of the player with another player usig the principle of the swap gate."""
    def __init__(self, color, max_cards=8):
        super().__init__(color, f"Quantum Superposed up to {max_cards}")
        self.max_cards = max_cards
        self.cardId=17
    
    def play(self, game):
        """Play the quantum swap card effect."""
        game.ui.set_info(f"{self.color} Quantum Swap Card played! Activating quantum effect...")
        self.activate_quantum_effect(game)
        game.ui.set_info("Hands swapped successfully.")
    def activate_quantum_effect(self, game,player1,player2):
        nbQubits = len(player1.hand) + len(player2.hand)
        circuit = QuantumCircuit(nbQubits+1)
        #apply hadamar gate to the first qubit it will be used as a control qubit
        circuit.h(0)
        for qubit in range(1, len(player1.hand)+1):
            circuit.x(qubit)  # Initialize qubits for player1's hand at 1
        for qubit in range (1, len(player1.hand)+1):  
            circuit.cswap(0, qubit,len(player1.hand)+qubit) 
        circuit.measure_all()
        # Run the circuit on a simulator backend
        backend = AerSimulator()
        circuit = transpile(circuit, backend)
        # Get the results of the measurement
        result = backend.run(circuit,shots=1).result()
        # Get the measured values (0 or 1)
        measured_values = result.get_counts(circuit)
        # Swap the hands of the players based on the measured values
        for i, value in enumerate(measured_values):
            #player 2 gets the cards where mesured value is 1
            game.player2.hand.extend([player1.hand.pop(i) for i in range(len(player1.hand)) if measured_values[value][i] == '1'])
            #player 1 gets the cards where measured value is 0 
            game.player1.hand.extend([player2.hand.pop(i) for i in range(len(player2.hand)) if measured_values[value][i] == '0'])
        game.ui.set_info(f"Swapped hands of {game.players[-1].name} and {game.players[0].name}.")
        
                
        


