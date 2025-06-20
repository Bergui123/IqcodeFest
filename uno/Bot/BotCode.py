from docplex.mp.model import Model
from qiskit_optimization.translators import from_docplex_mp
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.circuit.library import QAOAAnsatz
from qiskit_ibm_runtime import EstimatorV2 as Estimator, SamplerV2 as Sampler
from qiskit_aer import AerSimulator
from qiskit import transpile
from scipy.optimize import minimize
import numpy as np
from uno.QuantumCode.Player import Player
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_optimization.translators import to_ising

class BotCode(Player):
    def __init__(self, name="Bot"):
        super().__init__(name)
        self.is_bot = True

    def card_weight(self, card):
        if card.value == 'Draw Two':
            return 20
        elif card.value in ['Skip', 'Reverse']:
            return 10
        elif isinstance(card.value, int):
            return 1
        else:
            return 5

    def is_playable(self, card, top_card):
        return card.color == top_card.color or card.value == top_card.value

    def generate_qubo(self, Hand, top_card):
        mdl = Model("BotDecision")
        m = len(Hand)
        x = [mdl.binary_var(name=f"x_{i}") for i in range(m)]

        print(f"Hand: {[str(card) if self.is_playable(card, top_card) else 0 for card in Hand]}")
        weights = [self.card_weight(card) if self.is_playable(card, top_card) else 0 for card in Hand]

        obj = mdl.sum(-weights[i] * x[i] for i in range(m))
        constraint = mdl.sum(x) - 1
        alpha = 100
        mdl.minimize(obj + alpha * constraint * constraint)

        qp = from_docplex_mp(mdl)
        qubo = QuadraticProgramToQubo().convert(qp)
        return qubo, weights

    def cost_function(self, params, estimator, circuit, hamiltonian, pass_manager):
        isa_psi = pass_manager.run(circuit)
        isa_observables = hamiltonian.apply_layout(isa_psi.layout)
        job = estimator.run([(isa_psi, isa_observables, params)])
        cost = job.result()[0].data.evs
        return cost

    def decide_action(self, game):
        top_card = game.get_top_card()
        Hand = self.GetHand()

        if not Hand:
            return ('draw', None)

        qubo, weights = self.generate_qubo(Hand, top_card)
        hamiltonian, _ = to_ising(qubo)

        backend = AerSimulator()
        estimator = Estimator(mode=backend)
        pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=3)

        circuit_qaoa = QAOAAnsatz(hamiltonian, reps=10)
        p = circuit_qaoa.num_parameters // 2
        gamma_init = np.linspace(0.1, 1.5, p)
        beta_init = np.linspace(0.1, 1.5, p)
        params_init = np.concatenate([gamma_init, beta_init])

        res_opt = minimize(
            self.cost_function,
            params_init,
            args=(estimator, circuit_qaoa, hamiltonian, pass_manager),
            method="COBYLA"
        )

        params_opt = res_opt.x
        sampler = Sampler(mode=backend)

        circuit_meas = circuit_qaoa.decompose(reps=2).copy()
        circuit_meas.measure_all()

        counts = sampler.run([(circuit_meas, params_opt)]).result()[0].data.meas.get_counts()
        if isinstance(counts, dict):
            most_likely_bitstring = max(counts, key=counts.get)
        else:
            most_likely_bitstring = next(iter(counts), None)
            
        sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        most_likely_bitstring = sorted_counts[0][0] if len(sorted_counts) > 0 else None
        second_most_likely_bitstring = sorted_counts[1][0] if len(sorted_counts) > 1 else None
        if most_likely_bitstring == "0" * len(most_likely_bitstring):
            print("Most likely bitstring is all zeros, using second most likely.")
            most_likely_bitstring = second_most_likely_bitstring

        print(f"Most likely bitstring: {most_likely_bitstring}")

        # Indices jouables
        playable_indices = [i for i, card in enumerate(Hand) if self.is_playable(card, top_card)]

        if most_likely_bitstring is not None:
            selected_index = None
            max_weight = -1
            for i in range(len(playable_indices)):
                bit_val = int(most_likely_bitstring[::-1][i])
                real_index = playable_indices[i]
                print(f"Card {real_index}: {Hand[real_index]}, Bit: {bit_val}")
                if bit_val == 1:
                    return ('play', real_index)

            print("Bitstring has no 1s, fallback triggered.")
            for i in playable_indices:
                w = self.card_weight(Hand[i])
                if w > max_weight:
                    max_weight = w
                    selected_index = i

            if selected_index is not None:
                print(f"Fallback: manually selecting card {selected_index} -> {Hand[selected_index]}")
                return ('play', selected_index)

        print("No valid move, drawing a card.")
        return ('draw', None)

    def take_turn(self, game):
        idx = game.players.index(self)
        action, card_idx = self.decide_action(game)
        if action == 'play' and card_idx is not None:
            return game.play_card(idx, card_idx)
        return game.draw_card(idx)
