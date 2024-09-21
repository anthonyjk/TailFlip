import tkinter
from tkinter import ttk
import sv_ttk
from deck import Deck

deck = Deck('test')

def open_deck():
	deck.deck_display(root)

root = tkinter.Tk()

root.geometry("400x400")

# Sun Valley ttk theme
sv_ttk.set_theme("dark")

button = ttk.Button(root, text="Open Deck", command=open_deck)
button.pack()

root.mainloop()