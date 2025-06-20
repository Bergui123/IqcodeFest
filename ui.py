import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'uno'))
from uno.QuantumCode.GameController import Game
from uno.Bot.BotCode import BotCode
import random

class UnoGUI:
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.root.title("Quantum UNO")
        self.root.configure(bg="#1e1e1e")
        self.color_map = {"Red": "#ff6666", "Green": "#66ff66", "Blue": "#6666ff", "Yellow": "#ffff66"}
        self.name_font_size = 14
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
        bot = BotCode()
        self.game.players.append(bot)
        messagebox.showinfo("Bot Added", f"{bot.GetName()} has joined the game!")
        self.game.start()
        self.build_game_ui()
        self.update_ui()

    def build_game_ui(self):
        self.status_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.status_frame.pack(pady=5)

        self.name_label = tk.Label(
            self.status_frame, text="", font=(None, self.name_font_size, "bold"),
            fg="white", bg="#1e1e1e"
        )
        self.name_label.pack(side=tk.LEFT)

        self.turn_label = tk.Label(
            self.status_frame, text=" 's turn", font=(None, 14, "bold"),
            fg="#ffffff", bg="#1e1e1e"
        )
        self.turn_label.pack(side=tk.LEFT)

        self.top_card_label = tk.Label(
            self.root, text="", font=(None, 12), bg="#1e1e1e", fg="#dddddd"
        )
        self.top_card_label.pack(pady=5)

        self.cards_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.cards_frame.pack(pady=10)

        self.draw_button = tk.Button(
            self.root, text="Draw Card", command=self.draw_card,
            bg="#333333", fg="white", activebackground="#555555",
            relief=tk.RAISED, bd=2
        )
        self.draw_button.pack(pady=5)

        self.bot_area = tk.Frame(self.root, bg="#1e1e1e")
        self.bot_area.pack(pady=5)

        self.bot_label = tk.Label(
            self.bot_area, text="", font=(None, 12, "bold"),
            fg="white", bg="#1e1e1e"
        )
        self.bot_label.pack(anchor="w")

        self.bot_cards_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.bot_cards_frame.pack(pady=5)

    def update_ui(self):
        player = self.game.get_current_player()

        if isinstance(player, BotCode):
            self.bot_area.pack(pady=5)
            self.bot_cards_frame.pack(pady=5)
            self.bot_label.config(text="Bot is thinking...")
            self.root.update_idletasks()
            # Schedule bot action after 700 ms
            self.root.after(700, self.run_bot_turn)
            return  # Exit early to prevent immediate recursion

        self.bot_area.pack_forget()
        self.bot_cards_frame.pack_forget()

        self.name_label.config(text=player.GetName())
        top = self.game.get_top_card()
        color = self.color_map.get(top.color, "#dddddd")
        self.top_card_label.config(text=f"Top card: {top}", fg=color)

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for idx, card in enumerate(player.GetHand()):
            self.draw_card_canvas(self.cards_frame, card, idx)

    def run_bot_turn(self):
        player = self.game.get_current_player()
        self.update_bot_display()
        action, card = player.take_turn(self.game)
        if action == 'play':
            messagebox.showinfo("Bot Turn", f"{player.GetName()} plays {card}")
        elif action == 'draw':
            messagebox.showinfo("Bot Turn", f"{player.GetName()} draws {card}")
        else:
            messagebox.showwarning("Bot Turn", f"{player.GetName()} tried to draw but deck is empty.")
        self.game.next_turn()
        self.update_ui()

    def get_contrasting_text_color(self, bg_hex):
        bg_hex = bg_hex.lstrip('#')
        r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return "black" if brightness > 128 else "white"
    
    def draw_card_canvas(self, parent, card, index, is_clickable=True):
        card_color = self.color_map.get(card.color, "#cccccc")
        text_color = self.get_contrasting_text_color(card_color)

        canvas = tk.Canvas(parent, width=80, height=120, bg="#1e1e1e", highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=5)

        canvas.create_rectangle(5, 5, 75, 115, fill=card_color, outline="black", width=2)

        # Format text with automatic line wrapping and scaling
        name = str(card)
        if len(name) <= 10:
            font_size = 10
        elif len(name) <= 15:
            font_size = 9
        else:
            font_size = 8

        canvas.create_text(
            40, 60, text=name, fill=text_color,
            font=("Helvetica", font_size, "bold"),
            width=65, justify="center"
        )

        if is_clickable:
            canvas.tag_bind("all", "<Button-1>", lambda e: self.play_card(index))

    def update_bot_display(self):
        bot = self.game.players[-1]
        self.bot_label.config(text=f"{bot.GetName()}'s Hand:")
        for widget in self.bot_cards_frame.winfo_children():
            widget.destroy()
        for card in bot.GetHand():
            self.draw_card_canvas(self.bot_cards_frame, card, index=None, is_clickable=False)

    def play_card(self, idx):
        player = self.game.get_current_player()
        top = self.game.get_top_card()
        card = player.GetHand()[idx]
        if card.matches(top):
            if card.cardId == 17:  # Quantum Grover
                result = card.play(self.game)
                if result == "UI_SELECT":
                    self.prompt_grover_target(card, idx)
                    return
            else:
                self.game.play_card(self.game.current_player_idx, idx)
            winner = self.game.has_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner.GetName()} wins!")
                self.root.quit()
                return
            self.game.next_turn()
            self.show_name_spin()
            return
        else:
            messagebox.showwarning("Invalid Move", "Card does not match top card.")
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
        name = self.name_label.cget("text")
        steps = len(name)
        def spin(i):
            rotated = name[i:] + name[:i]
            self.name_label.config(text=rotated)
            if i < steps:
                self.root.after(100, lambda: spin(i+1))
            else:
                self.update_ui()
        spin(1)

    def prompt_grover_target(self, card_obj, card_index):
        player = self.game.get_current_player()
        hand = player.GetHand()

        window = tk.Toplevel(self.root)
        window.title("Select Card to Scan For")
        window.configure(bg="#222222")

        label = tk.Label(window, text="Choose a card to search for:", fg="white", bg="#222222")
        label.pack(pady=10)

        def on_select(target_index):
            selected_card = hand[target_index]
            window.destroy()
            self.game.get_card_by_idx(card_index).selected_card = selected_card
            self.game.play_card(self.game.current_player_idx, card_index)
            self.update_ui()

        for i, card in enumerate(hand):
            color = self.color_map.get(card.color, "#cccccc")
            btn = tk.Button(
                window,
                text=str(card),
                width=20,
                command=lambda i=i: on_select(i),
                bg=color,
                fg="black",
                activebackground=color,
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(padx=10, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    gui = UnoGUI(root)
    root.deiconify()
    root.mainloop()
