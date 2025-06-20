from cards.card import Card
from qiskit_aer import AerSimulator
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.circuit.library import QAOAAnsatz
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from scipy.optimize import minimize
from qiskit_optimization.translators import to_ising
import numpy as np


class QuantumBalanceCard(Card):
    def __init__(self, color="Purple"):
        super().__init__(color, "Quantum Balance")
        self.cardId = 14

    def card_weight(self, card):
        if isinstance(card.value, int):
            return card.value
        elif card.value == 'Skip':
            return 10
        elif card.value == 'Reverse':
            return 10
        elif card.value == 'Draw Two':
            return 15
        elif card.value == 'Quantum':
            return 20
        elif card.value == "DUMMY":
            return 0  # Dummy zero weight
        else:
            return 5

    def play(self, game):
        game.ui.set_info(f"{self.color} Quantum Balance Card played! Rebalancing hands quantumly...")

        players = [game.get_current_player(), game.get_next_player()]   #game.players[:2]
        all_cards = players[0].hand + players[1].hand

        dummy_used = False
        dummy_index = -1
        if len(all_cards) % 2 != 0:
            dummy_card = Card("Dummy", "DUMMY")
            all_cards.append(dummy_card)
            dummy_used = True
            dummy_index = len(all_cards) - 1

        n_cards = len(all_cards)

        # Build QUBO model where each variable x_i indicates which player owns card i:
        # x_i = 0 -> player 0, x_i = 1 -> player 1

        mdl = Model(name="Card_Player_Assignment")
        x = [mdl.binary_var(name=f"x_{i}") for i in range(n_cards)]

        weights = [self.card_weight(card) for card in all_cards]
        total_weight = sum(weights)
        avg_weight = total_weight / 2

        # Penalize difference in total weights:
        weight_diff = mdl.sum(weights[i] * x[i] for i in range(n_cards)) - avg_weight
        obj_weight = weight_diff * weight_diff

        # Penalize difference in number of cards assigned to each player:
        card_diff = mdl.sum(x) - n_cards / 2
        obj_card = card_diff * card_diff

        # Combine objectives with weighting factor alpha for card count balance
        alpha = 40
        mdl.minimize(obj_weight + alpha * obj_card)

        # Convert model to QUBO
        qp = from_docplex_mp(mdl)
        qubo = QuadraticProgramToQubo().convert(qp)

        # Convert to Ising Hamiltonian for quantum solver
        hamiltonian, _ = to_ising(qubo)

        backend = AerSimulator()
        estimator = Estimator(mode=backend)
        pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

        def cost_function(params, estimator, circuit, hamiltonian):
            # Run pass manager once
            isa_psi = pm.run(circuit)
            isa_observables = hamiltonian.apply_layout(isa_psi.layout)
            job = estimator.run([(isa_psi, isa_observables, params)])
            cost = job.result()[0].data.evs
            return cost

        circuit_qaoa = QAOAAnsatz(hamiltonian, reps=10)
        p = circuit_qaoa.num_parameters // 2
        gamma_init = np.linspace(0.1, 1.5, p)
        beta_init = np.linspace(0.1, 1.5, p)
        params_init = np.concatenate([gamma_init, beta_init])

        res_opt = minimize(
            cost_function,
            params_init,
            args=(estimator, circuit_qaoa, hamiltonian),
            method="COBYLA"
        )

        params_opt = res_opt.x

        sampler = Sampler(mode=backend)
        circuit_qaoa_copy = circuit_qaoa.decompose(reps=2).copy()
        circuit_qaoa_copy.measure_all()
        counts = sampler.run([(circuit_qaoa_copy, params_opt)]).result()[0].data.meas.get_counts()
        most_likely_bitstring = max(counts, key=counts.get)
        most_likely_bitstring = max(counts, key=counts.get)
        bitstring = most_likely_bitstring

        # If counts is dict, get most likely bitstring, else fallback
        if isinstance(counts, dict):
            most_likely_bitstring = max(counts, key=counts.get)
        else:
            # fallback (depends on sampler implementation)
            most_likely_bitstring = None
            for bitstring in counts:
                most_likely_bitstring = bitstring
                break

        if most_likely_bitstring is None:
            raise RuntimeError("Failed to get a bitstring from sampler result.")

        # Assign cards to players based on bitstring (reverse to match indexing)
        new_hands = {0: [], 1: []}
        for i in range(n_cards):
            if dummy_used and i == dummy_index:
                continue
            bit_val = int(most_likely_bitstring[::-1][i])
            new_hands[bit_val].append(all_cards[i])

        # Replace player hands
        for j, player in enumerate(players):
            player.hand = new_hands[j]

        game.ui.set_info("Quantum rebalance complete.")
