from uno.QuantumCode.Player import Player

class BotCode(Player):
    def __init__(self, name="Bot"):
        super().__init__(name)
        self.is_bot = True

    def get_hand(self):
        """Return the bot's current hand for decision-making."""
        return self.Hand

    def decide_action(self, game):
        """Determine action for the bot: ('draw', None) or ('play', card_index)."""
        # Always draw for now
        return ('draw', None)

    def take_turn(self, game):
        """Execute the bot's chosen action."""
        idx = game.players.index(self)
        action, card_idx = self.decide_action(game)
        if action == 'play' and card_idx is not None:
            return game.play_card(idx, card_idx)
        # default draw
        return game.draw_card(idx)
