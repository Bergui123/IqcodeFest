# deck.py
from cards.card import Card
from cards.quantum_card import QuantumCard
import random
import qrng  # Quantum Random Number Generator

from uno.cards import QuantumEnigma

colors = ['Red', 'Green', 'Blue', 'Yellow']
numbers = list(range(0, 10))
specials = ['Skip', 'Reverse', 'Draw Two']

def create_deck():
    deck = []
    for color in colors:
        deck.append(Card(color, 0))
        for num in range(1, 10):
            deck.append(Card(color, num))
            deck.append(Card(color, num))
        for sp in specials:
            deck.append(Card(color, sp))
            deck.append(Card(color, sp))
    # Add quantum cards
    deck.append(QuantumCard("Purple", "Quantum"))
    deck.append(QuantumCard("Purple", "Quantum"))
    deck.append(QuantumEnigma())
    #random.shuffle(deck)
    QuantumShuffleDeck(deck)
    return deck

def QuantumShuffleDeck(deck):
    """Shuffle the deck using quantum random numbers."""
    shuffled_deck = []
    qrng.set_provider_as_IBMQ('')
    qrng.set_backend()
    while deck:
        # Get a quantum random index
        index = qrng.get_random_int32(0, len(deck) - 1)
        shuffled_deck.append(deck.pop(index))
    return shuffled_deck
