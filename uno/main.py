# main.py
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(__file__)) 
from game import UnoGame
from ui import UnoUI

def main():
    root = tk.Tk()
    game = UnoGame(None)  # UI not set yet
    ui = UnoUI(root, game)
    game.ui = ui  # Circular reference for game to update UI
    root.mainloop()

if __name__ == "__main__":
    main()
