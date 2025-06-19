# ui.py
import tkinter as tk
from tkinter import messagebox
import random

class UnoUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.root.title("Uno Quantum Game")

        self.info_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        self.discard_label = tk.Label(root, text="Discard Pile", font=("Helvetica", 14))
        self.discard_label.pack(pady=5)

        self.discard_card_label = tk.Label(root, text="", font=("Helvetica", 18), width=15, relief="raised")
        self.discard_card_label.pack(pady=5)

        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack(pady=10)

        self.draw_button = tk.Button(root, text="Draw Card", command=self.player_draw_card)
        self.draw_button.pack(pady=5)

        self.update()

    def update(self):
        top_card = self.game.get_top_card()
        self.discard_card_label.config(text=str(top_card), bg=top_card.color.lower() if top_card.color.lower() in ['red','green','blue','yellow'] else 'purple')

        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(self.game.player.hand):
            btn = tk.Button(self.hand_frame, text=str(card), bg=card.color.lower() if card.color.lower() in ['red','green','blue','yellow'] else 'purple', width=12, command=lambda i=i: self.player_play_card(i))
            btn.pack(side=tk.LEFT, padx=5)

        if self.game.is_current_player_human():
            self.set_info("Your turn! Play a card or draw.")
            self.draw_button.config(state=tk.NORMAL)
        else:
            name = self.game.get_current_player().name # Update computer's hand for display
            self.set_info(f"{name} turn...")
            self.draw_button.config(state=tk.DISABLED)
            self.root.after(1500, self.computer_turn)

    def set_info(self, text):
        self.info_label.config(text=text)

    def player_play_card(self, index):
        if not self.game.is_current_player_human():
            return
        if self.game.play_card(self.game.player, index):
            winner = self.game.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.root.destroy()
                return
            self.game.advance_turn()
            self.update()
        else:
            messagebox.showinfo("Invalid Move", "Card does not match top card.")

    def player_draw_card(self):
        if not self.game.is_current_player_human():
            return
        card = self.game.draw_card(self.game.player)
        if card:
            self.set_info(f"You drew {card}")
        else:
            self.set_info("Deck is empty.")
        self.game.advance_turn()
        self.update()

    def computer_turn(self):
        if self.game.is_current_player_human():
            return
        valid_moves = [i for i, c in enumerate(self.game.computer.hand) if self.game.can_play(c)]
        if valid_moves:
            card_index = random.choice(valid_moves)
            card = self.game.computer.hand[card_index]
            self.game.play_card(self.game.computer, card_index)
            self.set_info(f"Computer played {card}")
        else:
            card = self.game.draw_card(self.game.computer)
            if card:
                self.set_info("Computer drew a card")
            else:
                self.set_info("Deck empty, computer cannot draw")

        winner = self.game.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.root.destroy()
            return

        self.game.advance_turn()
        self.update()