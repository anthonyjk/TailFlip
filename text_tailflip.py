from deck import Deck

exit = False

decks = []
def create_deck(name):
	decks.append(Deck(title))

def display_decks():
	print("""Deck List
---------
Index : Title""")
	for i in range(len(decks)):
		print(f'{i} : {decks[i].get_name()}')

def display_contents(index):
	decks[index].contents()

def create_card(index, front, back):
	decks[index].add_card([front, back])

print("Welcome to TailFlip!\n")
while exit == False:
	print("""\nType to access different menus.
c : create new deck
v : view decks
e : exit TailFlip\n""")

	opt = input(': ').lower()

	# Actions
	if opt == 'c':
		print("Title your new deck (type 'r' to return)")
		title = input(': ')

		if title.lower() != 'r':
			create_deck(title)
			print(f"Successfuly created new deck '{title}'")

	elif opt == 'v':
		display_decks()
		
		print("""Type for options
ci : create new card in deck (i = number)
vi : view deck contents (i = number)
di : cycle through cards
si : save deck to json
Enter : return
""")

		view_opt = list(input(': ').lower())
		# Watch out for incomplete inputs (ex: 'c' instead of 'c1')

		if len(view_opt) >= 2:
			try:
				index = int(''.join(view_opt[1:]))
			except:
				print("Provided index is not a valid integer.")
				view_opt = ''

			if view_opt[0] == 'c':
				print("Input front of card (leave blank to cancel):")
				f_card = input(': ')

				if f_card != '':
					print("Input back of card (leave blank to cancel):")
					b_card = input(': ')

					create_card(index, f_card, b_card)
					print(f"Successfully created new card in deck '{decks[index].get_name()}'!")

			elif view_opt[0] == 'v':
				display_contents(index)
				print("""\nr : remove card from deck
Enter : return""")
				card_opt = input(': ')

				if card_opt == 'r':
					print("\nType the first entry of the card to be removed (case sensitive)")
					remove = input(': ')
					decks[index].remove_card(remove)
					print(f"Successfully removed card from deck '{decks[index].get_name()}'!\n")

			elif view_opt[0] == 'd':
				decks[index].cycle()

			elif view_opt[0] == 's':
				decks[index].save_contents()
				print(f"Successfully saved '{decks[index].get_name()}' to '{decks[index].get_name()}.json'!")
		

	elif opt == 'e':
		exit = True



