import tkinter
from tkinter import ttk
import sv_ttk
from flip import Flip

flip = Flip('test')

flips = {}
click_x = 0
click_y = 0

def open_flip():
	"""
	Creates selection menu for Flip options to display
	"""
	def chosen_flip(event):
		"""
		Opens selected Flip display

		event: tkinter event
		"""
		widget = event.widget
		s_i = int(widget.curselection()[0]) # Select index
		name = widget.get(s_i)

		flips[name].flip_display(root, menu) # Deal with empty cards (dont display)

	menu = tkinter.Toplevel(root)
	menu.geometry('200x200')

	flip_select = tkinter.Listbox(menu, exportselection=False)
	flip_select.grid(sticky='nwes')

	index = 0
	for f in flips:
		flip_select.insert(index+1, f)
		index += 1

	flip_select.bind('<<ListboxSelect>>', chosen_flip)

def create_flip(name):
	"""
	Creates a new Flip object

	name: string name of new Flip object
	"""
	if name not in list(flips.keys()):
		flips[name] = Flip(name)
	else:
		print("Already exists") # Give an error message
	print(flips)

def flip_customize_window():
	"""
	Opens Flip customization window
	"""

	def pop_up_input():
		"""
		Creates text input window for new Flip creation
		"""

		def create_close():
			"""
			Creates new Flip and closes Flip creation window
			"""
			create_flip(input_text.get())
			update_list()
			pop.destroy()

		def cancel_close():
			"""
			closes Flip creation window without creating new Flip
			"""
			pop.destroy()

		pop = tkinter.Toplevel(root)
		pop.geometry(f"190x180+{root.winfo_x()+308}+{root.winfo_y()+350}")

		input_text = tkinter.StringVar()
		title = ttk.Entry(pop, width=25, textvariable=input_text)
		title.grid(row=0, column=0, columnspan=4, pady=(10,0), padx=10)

		ok_button = ttk.Button(pop, text='Create', command=create_close)
		ok_button.grid(row=1, column=2, sticky='nwe', columnspan=2, padx=(0,10))

		cancel_button = ttk.Button(pop, text='Cancel', command=cancel_close)
		cancel_button.grid(row=1, column=0, sticky='nwe', columnspan=2, padx=(10,0))

		pop.overrideredirect(True)

	contents = None # Setting up contents here so that the same window can be used
	word_list = None # To be accessed by both contents and create windows.
	def contents_window(name, first_load):
		"""
		Opens Flip contents window

		name: string name of Flip to be customized
		first_load: boolean if first open of contents window
		"""
		nonlocal contents, word_list

		def word_select(event):
			pass # TODO

		if first_load:
			contents = tkinter.Toplevel(window)
			contents.geometry("150x250")
		
		flip_label = ttk.Label(contents, text=name)
		flip_label.grid(row=0)

		contents.grid_rowconfigure(1, weight=1)
		word_list = tkinter.Listbox(contents, exportselection=False)
		word_list.grid(row=1, sticky='wnes')

		word_list.bind('<<ListboxSelect>>', word_select)

		index = 0
		for card in flips[name].get_cards():
			word_list.insert(index+1, card)
			index+=1

	create = None
	def card_create_window(name, first_load):
		"""
		Opens Flip card creation window

		name: string name of Flip to be customized
		first_load: boolean if first open of creation window
		"""
		nonlocal create, word_list

		def add_new_card():
			"""
			Adds new card to Flip object
			"""
			flips[name].add_card([front_text.get(), back_text.get()])
			length = len(flips[name].get_cards())
			word_list.insert(length, front_text.get())

		if first_load:
			create = tkinter.Toplevel(window)
			create.geometry("150x250")
		front_text = tkinter.StringVar()
		front_input = ttk.Entry(create, width=25, textvariable=front_text)
		front_input.grid(row=0)

		back_text = tkinter.StringVar()
		back_input = ttk.Entry(create, width=25, textvariable=back_text)
		back_input.grid(row=1)

		add_button = ttk.Button(create, text="Add", command=add_new_card)
		add_button.grid(row=2)

	def update_list():
		"""
		Adds new Flip to flip_list listbox
		"""
		nonlocal index
		flip_names = list(flips.keys())
		flip_list.insert(index+1, flip_names[index])
		index += 1

	select_i = -1
	first_load = True # First load of contents_window and card_create_window
	def on_select(event):
		"""
		Creates content and creation window of selected Flip from flip_list

		event: tkinter event
		"""
		nonlocal select_i, first_load

		widget = event.widget
		if int(widget.curselection()[0]) != select_i: # Prevents unnecessary reloading

			select_i = int(widget.curselection()[0]) # Select index
			flip_name = widget.get(select_i)

			contents_window(flip_name, first_load)
			card_create_window(flip_name, first_load)
			first_load = False

			print(f"Selected {flip_name}")

	window = tkinter.Toplevel(root)
	window.geometry("350x250")

	window.grid_columnconfigure(0, weight=1)
	window.grid_rowconfigure(1, weight=1)

	create_button = ttk.Button(window, text='Create Flip', command=pop_up_input)
	create_button.grid(row=0)

	flip_list = tkinter.Listbox(window, exportselection=False)
	flip_list.grid(row=1, sticky='wes')

	flip_list.bind('<<ListboxSelect>>', on_select)

	index = 0
	for f in flips:
		flip_list.insert(index+1, f)
		index += 1


def save_click_position(event):
	"""
	Saves last mouse click position on display

	event: tkinter event
	"""
	global click_x, click_y
	click_x = event.x
	click_y = event.y

def dragging(event):
	"""
	Updates display position from mouse drag

	event: tkinter event
	"""
	global click_x, click_y
	x = event.x - click_x
	y = event.y - click_y
	new_x = root.winfo_x() + x
	new_y = root.winfo_y() + y
	new_geom = f"+{new_x}+{new_y}"
	root.geometry(new_geom)

root = tkinter.Tk()

root.geometry("300x500")

# Sun Valley ttk theme
sv_ttk.set_theme("dark")
style = ttk.Style(root)
style.configure('title.TLabel', font=('Helvetica', 36))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=2)
#root.grid_columnconfigure(1, weight=1)

title_label = ttk.Label(text="TailFlip", style='title.TLabel')
title_label.grid(row=0)

button = ttk.Button(root, text="Open Flip", command=open_flip)
button.grid(row=1, sticky='nwes')


create_button = ttk.Button(root, text="Modify Flip", command=flip_customize_window)
create_button.grid(row=2, sticky='nwes')

#root.overrideredirect(True)
root.bind('<Button-1>', save_click_position)
root.bind('<B1-Motion>', dragging)
root.mainloop() 