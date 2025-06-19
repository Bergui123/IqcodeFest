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

    def AddPlayer(self, player):
        self.PlayerList.append(player)
        self.PLayerTurn.add(player)

    def RemovePlayer(self, player):
        if player in self.PlayerList:
            self.PlayerList.remove(player)

    def GetPlayers(self):
        return self.PlayerList
    def DrawCard(self,playerNumber):
        self.PlayerList[playerNumber].DrawCard(self.Deck.DrawCard())
    def PlayCard(self, playerNumber , cardIndex):
        if (self.PlayerList[playerNumber].GetCard is SpecialCard):
            
        else:

