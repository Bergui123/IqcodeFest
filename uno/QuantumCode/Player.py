class Player:
    def __init__(self, name):
        """Initialize the player with a name, an empty Hand, and an empty list of played cards."""
        self.Name = name
        self.Hand = []
        self.CardPlayed = []
        self.TurnNumber = None  # initialize turn number

    def AddCard(self, card):
        """Add a card to the player's Hand."""
        self.Hand.append(card)

    def PlayCard(self, card_index):
        """Play a card from the player's Hand by index."""
        if 0 <= card_index < len(self.Hand):
            card = self.Hand.pop(card_index)
            self.CardPlayed.append(card)
            return card
        else:
            raise IndexError("Invalid card index.")

    def DrawCard(self, card):
        """Add a card to the player's Hand."""
        self.Hand.append(card)

    def GetHand(self):
        """Return the player's Hand."""
        return self.Hand

    def GetName(self):
        """Return the player's name."""
        return self.Name

    def GetCardPlayed(self):
        """Return the cards played by the player."""
        return self.CardPlayed
    
    def GetCard(sef, cardIndex):
        return self.Hand[cardIndex] if 0 <= cardIndex < len(self.Hand) else None