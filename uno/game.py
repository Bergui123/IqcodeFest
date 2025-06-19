from deck import create_deck
from player_module import Player

class UnoGame:
    def __init__(self, ui):
        self.ui = ui
        self.deck = create_deck()
        self.discard_pile = []

        # Crée 4 joueurs : 1 humain, 3 ordinateurs
        self.players = [
            Player("You"),
            Player("Computer 1"),
            Player("Computer 2"),
            Player("Computer 3"),
        ]

        # Distribue 7 cartes à chaque joueur
        for _ in range(7):
            for player in self.players:
                player.draw_card(self.deck)

        # Pose la première carte dans la pile de défausse
        self.discard_pile.append(self.deck.pop())

        self.current_player_idx = 0
        self.turn_direction = 1  # 1 pour sens horaire, -1 pour sens antihoraire
        self.skip_next = False

    @property
    def player(self):
        # Le joueur humain est toujours le premier dans la liste
        return self.players[0]

    @property
    def computer(self):
        # Si ce n’est pas le tour du joueur humain, retourne le joueur ordinateur courant
        if not self.is_current_player_human():
            return self.players[self.current_player_idx]
        return None

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def reverse_turn_order(self):
        self.turn_direction *= -1

    def get_top_card(self):
        return self.discard_pile[-1]

    def can_play(self, card):
        return card.matches(self.get_top_card())

    def play_card(self, player, card_index):
        card = player.hand[card_index]
        if self.can_play(card):
            # Retire la carte de la main du joueur
            player.hand.pop(card_index)
            # Ajoute la carte sur la pile de défausse
            self.discard_pile.append(card)
            # Active l'effet de la carte
            card.play(self)
            self.ui.update()
            return True
        return False

    def draw_card(self, player):
        card = player.draw_card(self.deck)
        self.ui.update()
        return card

    def advance_turn(self):
        # Gère l'effet "skip"
        if self.skip_next:
            self.skip_next = False
            # On saute le joueur suivant
            self.current_player_idx = (self.current_player_idx + self.turn_direction) % len(self.players)

        # Passe au joueur suivant
        self.current_player_idx = (self.current_player_idx + self.turn_direction) % len(self.players)

    def next_player(self):
        return self.players[(self.current_player_idx + self.turn_direction) % len(self.players)]

    def check_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player.name
        return None

    def is_current_player_human(self):
        return self.get_current_player().name == "You"

    def get_player_hand(self, player):
        return player.hand
