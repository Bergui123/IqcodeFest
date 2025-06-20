from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from cards.card import Card

def card_to_index(card: Card, Hand: list[Card]) -> int:
    for i, c in enumerate(Hand):
        print(f"Checking card at index {i}: {c}")
        if c.color == card.color and c.value == card.value:
            return i
    return -1

def index_to_binary(index: int, num_qubits: int) -> str:
    return format(index, f"0{num_qubits}b")

def grover_oracle(target: str) -> QuantumCircuit:
    n = len(target)
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(target):
        if bit == '0':
            oracle.x(i)
    oracle.h(n-1)
    oracle.mcx(list(range(n-1)), n-1)
    oracle.h(n-1)
    for i, bit in enumerate(target):
        if bit == '0':
            oracle.x(i)
    oracle.name = "Oracle"
    return oracle

def diffusion_operator(n: int) -> QuantumCircuit:
    diff = QuantumCircuit(n)
    diff.h(range(n))
    diff.x(range(n))
    diff.h(n-1)
    diff.mcx(list(range(n-1)), n-1)
    diff.h(n-1)
    diff.x(range(n))
    diff.h(range(n))
    diff.name = "Diffusion"
    return diff

def grover_card_search(player_hand: list[Card], target_card: Card, verbose=True) -> bool:
    num_cards = len(player_hand)
    if num_cards == 0:
        return False
    num_qubits = (num_cards - 1).bit_length()

    card_index = card_to_index(target_card, player_hand)
    if card_index == -1:
        if verbose:
            print(f"The card {target_card} is not in the Hand.")
        return False

    target_bin = index_to_binary(card_index, num_qubits)
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.append(grover_oracle(target_bin), range(num_qubits))
    qc.append(diffusion_operator(num_qubits), range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))

    backend = AerSimulator()
    transpiled = transpile(qc, backend=backend)
    result = backend.run(transpiled, shots=1024).result()
    counts = result.get_counts()
    corrected_counts = {k[::-1]: v for k, v in counts.items()}
    top_result = max(corrected_counts, key=corrected_counts.get)

    if verbose:
        print(f"\nGrover result (corrected): {corrected_counts}")
        print(f"Top result (binary): {top_result} -> index {int(top_result, 2)}")

    return int(top_result, 2) == card_index
