from uno.QuantumCode.Deck import Deck


class Game:
    def __init__(self):
        """Initialize the game with an empty player list, turn list, and card in play."""
        self.PlayerList = []
        self.PlayerTurn = []
        self.CardInPlay = []
        self.Deck=Deck()
        self.TurnList=[]
        self.CurrentPlayerIndex=0
        self.TopCard=None

    def AddPlayer(self, player):
        self.PlayerList.append(player)
        self.PLayerTurn.add(player)
        self.CardInPlay.append(player.GetHand())

    def RemovePlayer(self, player):
        if player in self.PlayerList:
            self.PlayerList.remove(player)
        self.CardInPlay.remove(player.GetHand())

    def GetPlayers(self):
        return self.PlayerList
    
    def DrawCard(self,playerNumber):
        self.PlayerList[playerNumber].DrawCard(self.Deck.DrawCard())

    def PlayCard(self, playerNumber , cardIndex):
        if (self.PlayerList[playerNumber].GetCard is SpecialCard):
            card=self.PlayerList[playerNumber].PlayCard(cardIndex)
            card.execute()
        else:
            self.TopCard=self.PlayerList[playerNumber].PlayCard(cardIndex)

    def GetTopCard(self):
        """Return the top card in play."""
        return self.TopCard
    def SetTopCard(self, card):
        """Set the top card in play."""
        self.TopCard = card            
    def GetPlayerInfo(self, playerNumber):
        return self.PlayerList[playerNumber]
    