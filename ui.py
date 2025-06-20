import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'uno'))
from tkinter import simpledialog, messagebox
from uno.QuantumCode.GameController import Game
from uno.Bot.BotCode import BotCode
import random

class UnoGUI:
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.root.title("Quantum UNO")
        # Apply dark background, prepare color mappings and animations
        self.root.configure(bg="#1e1e1e")
        self.color_map = {"Red":"#ff6666","Green":"#66ff66","Blue":"#6666ff","Yellow":"#ffff66"}
        self.color_cycle = ["#ff4444","#44ff44","#4444ff","#ffff44"]
        self.cycle_index = 0
        # Initialize dynamic name font size
        self.name_font_size = 14
        # Setup phase
        self.setup_players()

    def setup_players(self):
        num = simpledialog.askinteger("Players", "Enter number of players (2-10):", minvalue=2, maxvalue=10)
        if num is None:
            self.root.destroy()
            return
        for i in range(num):
            name = simpledialog.askstring("Player Name", f"Enter name for player {i+1}:")
            if not name:
                name = f"Player{i+1}"
            self.game.add_player(name)
        # Add a bot that always draws
        bot = BotCode()
        self.game.players.append(bot)
        messagebox.showinfo("Bot Added", f"{bot.GetName()} has joined the game!")
        # Start game and build UI
        self.game.start()
        self.build_game_ui()
        self.update_ui()

    def build_game_ui(self):
        # Status with expanding player name and animated "'s turn"
        self.status_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.status_frame.pack(pady=5)
        self.name_label = tk.Label(self.status_frame, text="", font=(None, self.name_font_size, "bold"), fg="black", bg="#1e1e1e")
        self.name_label.pack(side=tk.LEFT)
        self.turn_label = tk.Label(self.status_frame, text=" 's turn", font=(None, 14, "bold"), fg="#ffffff", bg="#1e1e1e")
        self.turn_label.pack(side=tk.LEFT)
        self.top_card_label = tk.Label(self.root, text="", font=(None, 12), bg="#1e1e1e", fg="#dddddd")
        self.top_card_label.pack(pady=5)
        self.cards_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.cards_frame.pack(pady=10)
        self.draw_button = tk.Button(self.root, text="Draw Card", command=self.draw_card, bg="#333333", fg="white", activebackground="#555555")
        self.draw_button.pack(pady=5)
        # Removed name size/color animations
        # Bot Hand display
        self.bot_area = tk.Frame(self.root, bg="#1e1e1e")
        self.bot_area.pack(pady=5)
        self.bot_label = tk.Label(self.bot_area, text="", font=(None, 12, "bold"), fg="white", bg="#1e1e1e")
        self.bot_label.pack(anchor="w")
        self.bot_cards_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.bot_cards_frame.pack(pady=5)

    def update_ui(self):
        player = self.game.get_current_player()
        # Bot turn: show its Hand, draw and feedback
        if getattr(player, 'is_bot', False):
            # display bot Hand area and handle its action
            self.bot_area.pack(pady=5)
            self.bot_cards_frame.pack(pady=5)
            self.update_bot_display()
            # bot takes action
            action, card = player.take_turn(self.game)
            if action == 'play':
                messagebox.showinfo("Bot Turn", f"{player.GetName()} plays {card}")
            elif action == 'draw':
                if card:
                    messagebox.showinfo("Bot Turn", f"{player.GetName()} draws {card}")
                else:
                    messagebox.showwarning("Bot Turn", f"{player.GetName()} tried to draw but deck is empty.")
            self.game.next_turn()
            # update next turn UI
            self.update_ui()
            return
        # hide bot Hand when not bot turn
        self.bot_area.pack_forget()
        self.bot_cards_frame.pack_forget()
        # reset and render human player's UI
        self.name_font_size = 14
        self.name_label.config(font=(None, self.name_font_size, "bold"))
        top = self.game.get_top_card()
        # Update dynamic labels
        self.name_label.config(text=player.GetName())
        # Color the top card label text to match card color
        color = self.color_map.get(top.color, "#dddddd")
        self.top_card_label.config(text=f"Top card: {top}", fg=color)
        # Clear old buttons and ensure frame blends with theme
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        # Create card buttons
        for idx, card in enumerate(player.GetHand()):
            # Color-coded card buttons
            btn_color = self.color_map.get(card.color, "white")
            btn = tk.Button(
                self.cards_frame,
                text=str(card),
                width=15,
                bg=btn_color,
                fg="black",
                activebackground=btn_color,
                relief=tk.RAISED,
                bd=2,
                command=lambda i=idx: self.play_card(i)
            )
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.SUNKEN))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.pack(side=tk.LEFT, padx=4, pady=2)

    def update_bot_display(self):
        """Update the bot's Hand display in the UI."""
        bot = self.game.players[-1]  # Assuming the bot is the last player
        self.bot_label.config(text=f"{bot.GetName()}\'s Hand:")
        # Clear old bot card buttons
        for widget in self.bot_cards_frame.winfo_children():
            widget.destroy()
        # Create bot card buttons matching player style but disabled
        for card in bot.GetHand():
            btn_color = self.color_map.get(card.color, "white")
            btn = tk.Button(
                self.bot_cards_frame,
                text=str(card),
                width=15,
                fg="black",
                state=tk.DISABLED,
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=4, pady=2)

    def play_card(self, idx):
        player = self.game.get_current_player()
        top = self.game.get_top_card()
        card = player.GetHand()[idx]
        if card.matches(top):
            self.game.play_card(self.game.current_player_idx, idx)
            winner = self.game.has_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner.GetName()} wins!")
                self.root.quit()
                return
            # Advance turn then spin the name
            self.game.next_turn()
            self.show_name_spin()
            return
        else:
            messagebox.showwarning("Invalid Move", "Card does not match top card.")
        # No explosion on invalid, just refresh
        self.update_ui()

    def draw_card(self):
        drawn = self.game.draw_card(self.game.current_player_idx)
        if drawn:
            messagebox.showinfo("Card Drawn", f"You drew {drawn}")
        else:
            messagebox.showwarning("Deck Empty", "No cards left to draw.")
        self.game.next_turn()
        self.update_ui()

    def show_name_spin(self):
        """Rotate the player name text by cycling its characters to simulate spin."""
        name = self.name_label.cget("text")
        steps = len(name)
        def spin(i):
            rotated = name[i:] + name[:i]
            self.name_label.config(text=rotated)
            if i < steps:
                self.root.after(100, lambda: spin(i+1))
            else:
                # restore original and refresh UI for new player
                self.update_ui()
        spin(1)

if __name__ == "__main__":
    root = tk.Tk()
    # Hide empty main window until dialogs
    root.withdraw()
    gui = UnoGUI(root)
    root.deiconify()
    root.mainloop()
