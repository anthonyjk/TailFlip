import tkinter
from tkinter import ttk
import sv_ttk

class Deck:
	def __init__(self, name):
		self.name = name
		self.cards = {}

		self.is_displayed = False

	def get_cards(self):
		"""
		Returns card dictonary
		"""
		return self.cards

	def get_name(self):
		"""
		Returns deck name
		"""
		return self.name

	def set_name(self, new_name):
		"""
		Sets a new name for the deck
		"""
		self.name = new_name

	def add_card(self, card):
		"""
		Adds a new card to the deck

		card: array of size 2, [front_val, back_val]
		"""
		self.cards[card[0]] = card[1]

	def remove_card(self, card):
		"""
		Removes a card from the deck

		card: front value of card to be removed
		"""
		self.cards.pop(card)

	def contents(self):
		"""
		Prints the front and back of every card in the deck
		"""
		print(f'Deck: {self.name}')

		for k in self.cards.keys():
			print(f'{k} : {self.cards[k]}')

	def cycle(self):
		"""
		Runs a flip cycle through all cards currently in the deck
		"""
		print("Press Enter to flip.")
		print("Type 'n'/'p' for next/previous card.")
		print("type 'e' to exit.")

		i = 0 # Current card index
		exit = False
		front = True # Front or back of card
		keys = list(self.cards.keys())

		while exit == False:
			if front:
				print(f'\n{keys[i]}')
			else:
				print(f'\n{self.cards[keys[i]]}')
			opt = input(": ").lower()

			# Actions
			if opt == 'n':
				if(len(keys) != i + 1):
					front = True # Resetting card position
					i += 1

			elif opt == 'p':
				if(i-1 >= 0):
					front = True # Resetting card position
					i -= 1

			elif opt == 'e':
				exit = True

			else:
				front = not front # Flipping card

	def save_contents(self):
		f = open(self.name+".json", "w")
		for k in self.cards.keys():
			f.write(f'{k} : {self.cards[k]}\n')

	def deck_display(self, root):
		click_x = 0
		click_y = 0

		def close_deck():
			self.is_displayed = False
			window.destroy()

		def save_click_position(event):
			nonlocal click_x, click_y
			click_x = event.x
			click_y = event.y

		def dragging(event):
			nonlocal click_x, click_y
			x = event.x - click_x
			y = event.y - click_y
			new_x = window.winfo_x() + x
			new_y = window.winfo_y() + y
			new_geom = f"+{new_x}+{new_y}"
			window.geometry(new_geom)

		front = True
		def change_txt():
			nonlocal front
			front = not front
			if front:
				flashcard.configure(text="fa")
			else:
				flashcard.configure(text="tree")

		if self.is_displayed == False:
			self.is_displayed = True
			window = tkinter.Toplevel(root)

			style = ttk.Style(window)

			style.configure('card.TButton', font=('Helvetica',  24), relief='flat')

			exit_btn = ttk.Button(window, text="Exit", command=close_deck)
			exit_btn.pack()

			flashcard = ttk.Button(window, text="fa", command=change_txt, style='card.TButton', takefocus=False)
			flashcard.pack(fill = 'both', ipady=200)

			window.overrideredirect(True)
			window.geometry("600x300+500+300")
			window.bind('<Button-1>', save_click_position)
			window.bind('<B1-Motion>', dragging)
			window.mainloop()