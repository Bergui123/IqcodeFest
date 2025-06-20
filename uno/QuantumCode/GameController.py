import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from .Deck   import Deck
from .Player import Player
from cards.card import Card
import math

# explicit imports for every card in uno/cards/
from uno.cards.Quantum_color_card       import Quantum_color_card
from uno.cards.quantum_balance_card import quantum_balance_card
from uno.cards.quantum_card import quantum_card
from uno.cards.Quantum_draw_card       import Quantum_draw_card
from uno.cards.Quantum_grover_card import Quantum_grover_card
from uno.cards.Quantum_shuffle_card    import Quantum_shuffle_card
from uno.cards.Quantum_superposed_card import Quantum_superposed_card
from uno.cards.Quantum_swap_card      import Quantum_swap_card
from uno.cards.teleportation_card import teleportation_card
class Game:
    def __init__(self):
        """Initialize the game with an empty player list, turn list, and card in play."""
        self.deck = Deck()
        self.discard_pile = []
        self.players = []
        self.current_player_idx = 0
    def add_player(self, name):
        """Add a player by name."""
        self.players.append(Player(name))

    def build_deck(self):
        """Populate and shuffle the deck."""
        colors = ["Red", "Green", "Blue", "Yellow"]
        values = [str(n) for n in range(0, 10)]
        # Add number cards
        for color in colors:
            self.deck.CardInPile.append(Card(color, "0"))
            for v in values[1:]:
                self.deck.CardInPile.append(Card(color, v))
                self.deck.CardInPile.append(Card(color, v))

        #After some reflection, here is the repartition of the quantum cards that I think is the best:
        # 6 Quantum_color_card (without color)
        # 8 Quantum_draw_card (2 for each color)
        # 4 Quantum_superposed_card (1 for each color)
        # 2 Quantum_swap_card (without color)
        # 2 Quantum_shuffle_card (without color)
        # 2 quantum_balance_card (without color)
        # 8 quantum_card (2 for each color)
        # 4 Quantum_grover_card (1 for each color)
        # 4 teleportation_card (1 for each color)
        self.deck.CardInPile.append(Quantum_color_card(["Red", "Blue", "Green", "Yellow"],"Quantum"))
        self.deck.CardInPile.append(Quantum_color_card(["Red", "Blue", "Green", "Yellow"],"Quantum"))
        self.deck.CardInPile.append(Quantum_color_card(["Red", "Blue", "Green", "Yellow"],"Quantum"))
        self.deck.CardInPile.append(Quantum_color_card(["Red", "Blue", "Green", "Yellow"],"Quantum"))
        self.deck.CardInPile.append(Quantum_draw_card("Red", 8))
        self.deck.CardInPile.append(Quantum_draw_card("Blue", 8))
        self.deck.CardInPile.append(Quantum_draw_card("Green", 8))
        self.deck.CardInPile.append(Quantum_draw_card("Yellow", 8))
        self.deck.CardInPile.append(Quantum_superposed_card("Red"))
        self.deck.CardInPile.append(Quantum_superposed_card("Blue"))
        self.deck.CardInPile.append(Quantum_superposed_card("Green"))
        self.deck.CardInPile.append(Quantum_superposed_card("Yellow"))
        self.deck.CardInPile.append(Quantum_swap_card("Red"))
        self.deck.CardInPile.append(Quantum_swap_card("Blue"))
        self.deck.CardInPile.append(Quantum_swap_card("Green"))
        self.deck.CardInPile.append(Quantum_swap_card("Yellow"))
        self.deck.CardInPile.append(Quantum_shuffle_card("Red"))
        self.deck.CardInPile.append(Quantum_shuffle_card("Blue"))
        self.deck.CardInPile.append(Quantum_shuffle_card("Green"))
        self.deck.CardInPile.append(Quantum_shuffle_card("Yellow"))
        # self.deck.CardInPile.append(quantum_balance_card("Red"))
        # self.deck.CardInPile.append(quantum_balance_card("Blue"))
        # self.deck.CardInPile.append(quantum_balance_card("Green"))
        # self.deck.CardInPile.append(quantum_balance_card("Yellow"))
        self.deck.CardInPile.append(quantum_card("Red"))
        self.deck.CardInPile.append(quantum_card("Blue"))
        self.deck.CardInPile.append(quantum_card("Green"))
        self.deck.CardInPile.append(quantum_card("Yellow"))
        self.deck.CardInPile.append(Quantum_grover_card("Red"))
        self.deck.CardInPile.append(Quantum_grover_card("Blue"))
        self.deck.CardInPile.append(Quantum_grover_card("Green"))
        self.deck.CardInPile.append(Quantum_grover_card("Yellow"))
        self.deck.CardInPile.append(teleportation_card("Red"))
        self.deck.CardInPile.append(teleportation_card("Blue"))
        self.deck.CardInPile.append(teleportation_card("Green"))
        self.deck.CardInPile.append(teleportation_card("Yellow"))

        self.QuantumShuffleDeck()
        # random.shuffle(self.deck.CardInPile)

    def deal(self):
        """Deal 7 cards to each player"""
        for _ in range(7):
            for player in self.players:
                if self.deck.CardInPile:
                    player.AddCard(self.deck.CardInPile.pop(0))

    def start(self):
        """Initial setup: build deck, deal, and flip first card."""
        self.build_deck()
        self.deal()
        # flip first card
        if self.deck.CardInPile:
            first = self.deck.CardInPile.pop(0)
            self.discard_pile.append(first)

    def get_current_player(self):
        return self.players[self.current_player_idx]
    
    def get_next_player(self):
        return self.players[(self.current_player_idx + 1) % len(self.players)]

    def get_top_card(self):
        return self.discard_pile[-1] if self.discard_pile else None

    def draw_card(self, player_idx):
        """Controller handles drawing a card."""
        if self.deck.CardInPile:
            card = self.deck.CardInPile.pop(0)
            self.players[player_idx].AddCard(card)
            return card
        return None

    def play_card(self, player_idx, card_idx):
        """Controller handles playing a card."""
        played = self.players[player_idx].PlayCard(card_idx)
        played.play(self)
        self.discard_pile.append(played)
        return played

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def quantum_detect_winner_index(self):
        """
        Simule un circuit quantique où l'index du joueur avec main vide est encodé en binaire.
        Suppose qu'un seul joueur a une main vide.
        """
        num_players = len(self.players)
        num_qubits = (num_players - 1).bit_length()

        # Cherche index du joueur gagnant
        winner_index = None
        for i, player in enumerate(self.players):
            if not player.GetHand():
                winner_index = i
                break

        if winner_index is None:
            return None  # Aucun gagnant

        # Encode l’index dans un registre quantique
        qc = QuantumCircuit(num_qubits, num_qubits)
        bin_index = format(winner_index, f'0{num_qubits}b')

        for i, bit in enumerate(reversed(bin_index)):
            if bit == '1':
                qc.x(i)

        qc.measure(range(num_qubits), range(num_qubits))

        sim = AerSimulator()
        qc = transpile(qc, sim)
        result = sim.run(qc, shots=1).result()
        counts = result.get_counts()

        measured = list(counts.keys())[0]
        return int(measured, 2)  # Reverse for Qiskit's LSB convention

    def has_winner(self):
        """Return winning player or None."""
        idx = self.quantum_detect_winner_index()
        if idx is not None:
            return self.players[idx]
        return None
    

    def QuantumShuffleDeck(self):
        """Shuffle the deck using quantum-generated indices."""
        shuffled_deck = []
        sim = AerSimulator()

        while self.deck.CardInPile:
            # Update number of cards remaining
            num_cards = len(self.deck.CardInPile)

            # Handle the final card without quantum circuit
            if num_cards == 1:
                shuffled_deck.append(self.deck.CardInPile.pop(0))
                break

            # Dynamically calculate number of qubits needed (at least 1)
            n_qubits = max(1, math.ceil(math.log2(num_cards)))

            # Build quantum circuit
            qc = QuantumCircuit(n_qubits, n_qubits)
            qc.h(range(n_qubits))  # apply Hadamard to all qubits
            qc.measure(range(n_qubits), range(n_qubits))

            # Transpile and run
            tqc = transpile(qc, sim)
            job = sim.run(tqc, shots=1)
            result = job.result()
            counts = result.get_counts()
            bitstring = list(counts.keys())[0]

            try:
                index = int(bitstring, 2) % num_cards
            except ValueError:
                index = random.randint(0, num_cards - 1)

            # Append selected card and remove from original deck
            shuffled_deck.append(self.deck.CardInPile.pop(index))

        self.deck.CardInPile = shuffled_deck


    def reverse_turn_order(self):
        """Reverse the turn order of players."""
        self.players.reverse()
        self.current_player_idx = len(self.players) - 1 - self.current_player_idx

    def get_card_by_idx(self, card_idx):
        player = self.get_current_player()
        if 0 <= card_idx < len(player.Hand):
            return player.Hand[card_idx]
        return None
        