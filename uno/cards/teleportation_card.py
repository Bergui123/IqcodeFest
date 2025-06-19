from cards.card import Card
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator  # or from qiskit.providers.aer import AerSimulator

import random

class TeleportationCard(Card):
    def __init__(self, color):
        super().__init__(color, "Teleportation")
    
    def play(self, game):
        game.ui.set_info(f"{self.color} Teleportation Card played! Activating quantum teleportation...")
        
        # Run the teleportation circuit
        measurement = self.activate_teleportation()
        
        # Interpret measurement outcome (bitstring like '00', '01', '10', or '11')
        ones_count = measurement.count('1')
        
        # For example, swap cards between current and next player equal to number of 1s (max 2)
        num_swaps = ones_count
        
        if num_swaps == 0:
            game.ui.set_info("Teleportation succeeded flawlessly! No cards swapped.")
            return
        
        curr_player = game.current_player
        next_player = game.next_player
        
        swaps_done = []
        
        for _ in range(num_swaps):
            if not curr_player.hand or not next_player.hand:
                break
            
            # Pick random cards to swap
            card_from_curr = random.choice(curr_player.hand)
            card_from_next = random.choice(next_player.hand)
            
            curr_player.hand.remove(card_from_curr)
            next_player.hand.remove(card_from_next)
            
            curr_player.hand.append(card_from_next)
            next_player.hand.append(card_from_curr)
            
            swaps_done.append((str(card_from_curr), str(card_from_next)))
        
        msg = f"Teleportation swapped {len(swaps_done)} cards between {curr_player.name} and {next_player.name}:\n"
        msg += "\n".join([f"{curr} <--> {nxt}" for curr, nxt in swaps_done])
        
        game.ui.set_info(msg)
        game.ui.update()
    
    def activate_teleportation(self):
        qc = QuantumCircuit(3, 2)
        
        # Prepare |+> state to teleport (can be changed)
        qc.h(0)
        
        # Create Bell pair between qubit 1 and 2
        qc.h(1)
        qc.cx(1, 2)
        
        # Bell measurement on qubit 0 and 1
        qc.cx(0, 1)
        qc.h(0)
        
        qc.measure([0, 1], [0, 1])
        
        sim = AerSimulator()
        qc = transpile(qc, sim)
        job = sim.run(qc)
        result = job.result()
        counts = result.get_counts()
        
        # Return the measurement bitstring (e.g. '00', '01', '10', or '11')
        measurement = list(counts.keys())[0]
        print(f"Teleportation measurement: {measurement}")
        return measurement
