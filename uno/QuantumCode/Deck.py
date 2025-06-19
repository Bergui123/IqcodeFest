class Deck:

    def __init__(self):
        """Initialize the deck with an empty pile and discard list."""
        self.CardInPile = []
        self.CardDiscarted = []
        self.AllTheCardType = []
    def PlayCard(self, card):
        # move a played card to discard pile
        self.CardDiscarted.append(card)
    def AddCard(self, card):
        """Add a card to the deck."""
        self.CardInPile.append(card)
    def DrawCard(self):
        # draw top card from pile
        return self.CardInPile.pop(0) if self.CardInPile else None
    def GetPileSize(self):
        """Return the number of cards in the pile."""
        return len(self.CardInPile)