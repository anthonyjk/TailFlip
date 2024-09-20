class Deck:
	def __init__(self, name):
		self.name = name
		self.cards = {}

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