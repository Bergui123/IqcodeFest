# deck.py
from cards.card import Card
from cards.quantum_card import QuantumCard
import random

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
    random.shuffle(deck)
    return deck
