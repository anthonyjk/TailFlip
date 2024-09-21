import tkinter
from tkinter import ttk
import sv_ttk

class Flip:
"""
Flip class to create Flip objects which contain flashcards
"""
	def __init__(self, name):
		"""
		Initializes attributes

		name: string name of the Flip
		"""
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
		Returns Flip name
		"""
		return self.name

	def set_name(self, new_name):
		"""
		Sets a new name for the Flip

		new_name: string of the Flip's new name
		"""
		self.name = new_name

	def add_card(self, card):
		"""
		Adds a new card to the Flip

		card: array of size 2, [front_val, back_val]
		"""
		self.cards[card[0]] = card[1]

	def remove_card(self, card):
		"""
		Removes a card from the Flip

		card: front value of card to be removed
		"""
		self.cards.pop(card)

	def contents(self):
		"""
		Prints the front and back of every card in the Flip
		"""
		print(f'Flip: {self.name}')

		for k in self.cards.keys():
			print(f'{k} : {self.cards[k]}')

	def cycle(self):
		"""
		Terminal-based flashcard viewer
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
		"""
		Saves word contents to json file
		"""
		f = open(self.name+".json", "w")
		for k in self.cards.keys():
			f.write(f'{k} : {self.cards[k]}\n')

	def flip_display(self, root, menu):
		"""
		Creates flashcard display of the Flip

		root: Tkinter root of program
		menu: Tkinter selection window
		"""
		menu.update()
		menu.destroy()

		click_x = 0
		click_y = 0

		def close_flip():
			"""
			Closes Flip display
			"""
			self.is_displayed = False
			window.destroy()

		def save_click_position(event):
			"""
			Saves last mouse click position on display

			event: tkinter event
			"""
			nonlocal click_x, click_y
			click_x = event.x
			click_y = event.y

		def dragging(event):
			"""
			Updates display position from mouse drag

			event: tkinter event
			"""
			nonlocal click_x, click_y
			x = event.x - click_x
			y = event.y - click_y
			new_x = window.winfo_x() + x
			new_y = window.winfo_y() + y
			new_geom = f"+{new_x}+{new_y}"
			window.geometry(new_geom)

		card_index = 0
		card_list = list(self.cards.keys())
		text = "There are no cards in this deck."
		front = True
		def flip_card():
			"""
			Updates Flashcard text with corresponding word pair
			"""
			nonlocal front, card_index
			front = not front
			if len(self.cards) > 0:
				if front:
					text = card_list[card_index]
				else:
					text = self.cards[card_list[card_index]]
				flashcard.configure(text=text)

		def update_card():
			"""
			Updates Flashcard text to front word of current word index
			"""
			nonlocal front, card_index
			front = True
			text = card_list[card_index]
			flashcard.configure(text=text)

		def move_left():
			"""
			Moves card index left if possible
			"""
			nonlocal card_index
			if card_index > 0:
				card_index -= 1
				update_card()

		def move_right():
			"""
			Moves card index right if possible
			"""
			nonlocal card_index
			if card_index < len(self.cards) - 1:
				card_index += 1
				update_card()

		if self.is_displayed == False:
			self.is_displayed = True
			window = tkinter.Toplevel(root)

			style = ttk.Style(window)

			style.configure('card.TButton', font=('Helvetica',  24), relief='flat')
			style.configure('arrow.TButton', relief='flat')

			exit_btn = ttk.Button(window, text="Exit", command=close_flip)
			exit_btn.grid(row=0, column=0, sticky='w')

			left_btn = ttk.Button(window, text="<", style='arrow.TButton', takefocus=False, command=move_left)
			left_btn.grid(row=0, column=2, sticky='e')

			right_btn = ttk.Button(window, text=">", style='arrow.TButton', takefocus=False, command=move_right)
			right_btn.grid(row=0, column=3, sticky='e')

			window.grid_rowconfigure(1, weight=1)
			window.grid_columnconfigure(2, weight=1)

			if len(self.cards) > 0:
				text = card_list[card_index]
			flashcard = ttk.Button(window, text=text, command=flip_card, style='card.TButton', takefocus=False)
			flashcard.grid(row=1, column=0, columnspan=4, sticky='nesw')

			window.overrideredirect(True) # TODO: Add frame to let user resize flip.
			window.geometry("500x300+500+300")
			window.bind('<Button-1>', save_click_position)
			window.bind('<B1-Motion>', dragging)
			window.mainloop()