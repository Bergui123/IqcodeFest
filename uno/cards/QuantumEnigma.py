import random

class QuantumEnigma:
    questions = [
    "What is the basic unit of quantum information?",
    "What is the name of the quantum phenomenon where qubits influence each other instantly?",
    "Which gate creates superposition?",
    "Which gate is like a NOT gate in quantum computing?",
    "What is the result of measuring a qubit in superposition?",
    "How many states can a qubit be in at once?",
    "Which gate flips a qubit if the control is 1?",
    "What is the opposite of coherence in quantum systems?",
    "What kind of computer uses qubits?",
    "What is the Pauli-X gate also called?"
    ]

    answers = [
    "qubit",
    "entanglement",
    "Hadamard",
    "Pauli-X",
    "0 or 1",
    "two",
    "CNOT",
    "decoherence",
    "quantum",
    "NOT"
    ]
    cardId=16
    # Pair them using zip
    qa_pairs = list(zip(questions, answers))
    current_question=None
    current_answer=None
    def __init__(self):
        self.current_question = None
        self.current_answer = None
        self.select_random_qa()  # Automatically select a random pair on initialization
    
    def select_random_qa(self):
        """Select a random question-answer pair and assign to current attributes."""
        random_pair = random.choice(self.qa_pairs)
        self.current_question = random_pair[0]
        self.current_answer = random_pair[1]
    def get_question(self):
        """Return the current question."""
        return self.current_question
    
    def get_answer(self):
        """Return the current answer."""
        return self.current_answer
    
    def check_answer(self, answer):
        """Check if the provided answer matches the current answer."""
        return answer.lower() == self.current_answer.lower()
    
    def reset(self):
        """Reset the game by selecting a new random question-answer pair."""
        self.select_random_qa()
    def get_card_id(self):
        """Return the unique ID of the card."""
        return self.cardId
    