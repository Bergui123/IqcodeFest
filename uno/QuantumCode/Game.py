from qiskit import QuantumCircuit
from uno.QuantumCode.Deck import Deck
import random
from uno.QuantumCode.Player import Player
from uno.cards.card import Card
from qiskit_aer import AerSimulator # new simulator backend replacing BasicAer
from qiskit import transpile


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
        random.shuffle(self.deck.CardInPile)

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
        self.discard_pile.append(played)
        return played

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def has_winner(self):
        """Return winning player or None."""
        for player in self.players:
            if not player.GetHand():
                return player
        return None
    
    def QuantumShuffleDeck(self):
        """Shuffle the deck using quantum principles."""
        shuffled_deck = []
        """Generate a quantum random number between 0 and max_cards (inclusive)."""
        n_qubits = 3  #
        qc = QuantumCircuit(n_qubits, n_qubits)

        # Put all qubits into superposition
        for q in range(n_qubits):
            qc.h(q)

        qc.measure(range(n_qubits), range(n_qubits))
        sim = AerSimulator()    
        qc = transpile(qc, sim)
        job = sim.run(qc)
        result = job.result()
        counts = result.get_counts()

        bitstring = list(counts.keys())[0]
        number = int(bitstring, 2)
        
        while self.deck:
            shuffled_deck.append(self.deck.pop(number% len(self.deck)))
        self.deck = shuffled_deck

