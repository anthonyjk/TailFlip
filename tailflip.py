import tkinter
from tkinter import ttk
import sv_ttk
from flip import Flip
import flips_data as fd
import flip_visual as fv

flip = Flip('test')

flips = {}
click_x = 0
click_y = 0

window = None
create = None
contents = None

def open_flip():
	"""
	Creates selection menu for Flip options to display
	"""

	# Saving current flips
	for flip in flips.values():
		fd.download_flip(flip)

	global window, create, contents
	def chosen_flip(event):
		"""
		Opens selected Flip display

		event: tkinter event
		"""
		widget = event.widget
		s_i = int(widget.curselection()[0]) # Select index
		name = widget.get(s_i)

		flips[name].flip_display(root, menu) # Deal with empty cards (dont display)

	#def save_flips():
	#	for flip in flips:
	#		flip.save_contents()

	try:
		window.destroy()
		create.destroy()
		contents.destroy()

		window = None
		create = None
		contents = None
	except:
		pass

	menu = tkinter.Toplevel(root)
	menu.geometry('200x200')

	menu.grid_columnconfigure(0, weight=1)
	menu.grid_rowconfigure(0, weight=1)

	flip_select = tkinter.Listbox(menu, exportselection=False)
	flip_select.grid(row=0,column=0,sticky='nwes')
	flip_select.config(font=('Tahoma', 10), justify=tkinter.CENTER)

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

def flip_customize_window():
	"""
	Opens Flip customization window
	"""
	global window

	if window != None:
		if window.winfo_exists():
			return

	def pop_up_input():
		"""
		Creates text input window for new Flip creation
		"""

		def create_close():
			"""
			Creates new Flip and closes Flip creation window
			"""
			if(len(input_text.get().strip(' ')) > 0):
				create_flip(input_text.get())
				update_list()
				pop.destroy()

		def cancel_close():
			"""
			closes Flip creation window without creating new Flip
			"""
			pop.destroy()

		pop = tkinter.Toplevel(root)
		pop.geometry(f"190x80+{window.winfo_x()+80}+{window.winfo_y()+65}")

		input_text = tkinter.StringVar()
		title = ttk.Entry(pop, width=25, textvariable=input_text)
		title.grid(row=0, column=0, columnspan=4, pady=(10,0), padx=10)

		ok_button = ttk.Button(pop, text='Create', command=create_close)
		ok_button.grid(row=1, column=2, sticky='nwe', columnspan=2, padx=(0,10))

		cancel_button = ttk.Button(pop, text='Cancel', command=cancel_close)
		cancel_button.grid(row=1, column=0, sticky='nwe', columnspan=2, padx=(10,0))

		#pop.overrideredirect(True)

	word_list = None # To be accessed by both contents and create windows.
	front_input = None
	back_input = None
	add_button = None
	replace_index = None
	flip_label = None
	old_card = ""
	def contents_window(name, first_load):
		"""
		Opens Flip contents window

		name: string name of Flip to be customized
		first_load: boolean if first open of contents window
		"""
		global contents
		nonlocal flip_label, word_list, front_input, back_input, add_button, old_card, replace_index

		def word_select(event):
			nonlocal replace_index, old_card
			widget = event.widget
			replace_index = int(widget.curselection()[0]) # Select index
			name = widget.get(replace_index)
			if name == "Create New Card":
				add_button.config(text='Add')
				front_input.delete(0, tkinter.END)
				front_input.insert(0, "")

				back_input.delete(0, tkinter.END)
				back_input.insert(0, "")
			else:
				add_button.config(text='Update')
				new_text = name.split(' | ')
				old_card = new_text[0]

				front_input.delete(0, tkinter.END)
				front_input.insert(0, new_text[0])

				back_input.delete(0, tkinter.END)
				back_input.insert(0, new_text[1])

		if first_load:
			contents = tkinter.Toplevel(window)
			contents.geometry(f"175x250+{root.winfo_x()+308}+{root.winfo_y()+280}")
			contents.overrideredirect(True)
		
		try:
			flip_label.config(text=name)
		except:
			style.configure('flip_name.TLabel', font=('Tahoma', 12))
			flip_label = ttk.Label(contents, text=name, style='flip_name.TLabel')
			flip_label.grid(row=0)

		contents.grid_columnconfigure(0, weight=1)
		contents.grid_rowconfigure(1, weight=1)
		word_list = tkinter.Listbox(contents, exportselection=False)
		word_list.grid(row=1, sticky='wnes')
		word_list.config(font=('Tahoma', 10))

		word_list.bind('<<ListboxSelect>>', word_select)

		contents.bind('<Button-1>', save_click_position)
		contents.bind('<B1-Motion>', window_dragging)

		index = 0
		word_list.insert(0, 'Create New Card')
		for card in flips[name].get_cards():
			word_list.insert(index+1, f'{card} | {flips[name].get_cards()[card]}')
			index+=1

	def card_create_window(name, first_load):
		"""
		Opens Flip card creation window

		name: string name of Flip to be customized
		first_load: boolean if first open of creation window
		"""
		global create
		nonlocal word_list, front_input, back_input, add_button, old_card, replace_index

		def add_new_card():
			"""
			Adds new card to Flip object
			"""
			if add_button.cget('text') == 'Add':
				if len(front_text.get().strip(' ')) > 0 and len(back_text.get().strip(' ')) > 0:
					flips[name].add_card([front_text.get(), back_text.get()])
					length = len(flips[name].get_cards())
					word_list.insert(length, f'{front_text.get()} | {back_text.get()}')

					front_input.delete(0, tkinter.END)
					front_input.insert(0, "")

					back_input.delete(0, tkinter.END)
					back_input.insert(0, "")

					save_current_flip(flips[name])
			elif add_button.cget('text') == 'Update':
				flips[name].replace_card(old_card, [front_text.get(), back_text.get()], replace_index)
				word_list.delete(replace_index)
				word_list.insert(replace_index, f'{front_text.get()} | {back_text.get()}')

				# Reset back to adding a card
				front_input.delete(0, tkinter.END)
				front_input.insert(0, "")

				back_input.delete(0, tkinter.END)
				back_input.insert(0, "")

				add_button.config(text='Add')

				save_current_flip(flips[name])

		def remove_card():
			nonlocal old_card
			if old_card != '':
				flips[name].remove_card(old_card)
				word_list.delete(replace_index)

				front_input.delete(0, tkinter.END)
				front_input.insert(0, "")

				back_input.delete(0, tkinter.END)
				back_input.insert(0, "")

				add_button.config(text='Add')
				old_card = ''

				save_current_flip(flips[name])

		def save_current_flip(flip):
			fd.download_flip(flip)


		if first_load:
			create = tkinter.Toplevel(window)
			create.geometry(f"175x250+{root.winfo_x()+482}+{root.winfo_y()+280}")
			create.overrideredirect(True)

		create.grid_columnconfigure(0, weight=1)

		front_text = tkinter.StringVar()
		front_input = ttk.Entry(create, width=25, textvariable=front_text)
		front_input.grid(row=0,column=0)

		back_text = tkinter.StringVar()
		back_input = ttk.Entry(create, width=25, textvariable=back_text)
		back_input.grid(row=1,column=0)

		add_button = ttk.Button(create, text="Add", command=add_new_card)
		add_button.grid(row=2,column=0, sticky='we')

		delete_button = ttk.Button(create, text="Delete", command=remove_card)
		delete_button.grid(row=3,column=0, sticky='we')

		create.bind('<Button-1>', save_click_position)
		create.bind('<B1-Motion>', window_dragging)

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
	flip_name = ""
	def on_select(event):
		"""
		Creates content and creation window of selected Flip from flip_list

		event: tkinter event
		"""
		nonlocal select_i, first_load, flip_name

		widget = event.widget
		if int(widget.curselection()[0]) != select_i: # Prevents unnecessary reloading

			select_i = int(widget.curselection()[0]) # Select index
			flip_name = widget.get(select_i)

			contents_window(flip_name, first_load)
			card_create_window(flip_name, first_load)
			first_load = False

			print(f"Selected {flip_name}")

	def delete_flip():
		global create, contents
		nonlocal flip_name, select_i, index, first_load
		# TODO: Make a "Are you sure?" pop-up

		if flip_name != "":
			flip_list.delete(select_i)
			flips.pop(flip_name)
			fd.delete_file(flip_name)
			index -= 1
			select_i = -1
			first_load = True

		if create != None and contents != None:
			create.destroy()
			contents.destroy()

	def window_dragging(event):
		"""
		Updates display position from mouse drag

		event: tkinter event
		"""
		selected_widget = event.widget.focus_get()
		if isinstance(selected_widget, tkinter.Entry):
			return "break"

		global click_x, click_y, contents, create
		x = event.x - click_x
		y = event.y - click_y
		new_x = window.winfo_x() + x
		new_y = window.winfo_y() + y
		root_x = root.winfo_x() + x
		root_y = root.winfo_y() + y
		new_geom = f"+{new_x}+{new_y}"
		root_geom = f"+{root_x}+{root_y}"
		window.geometry(new_geom)
		root.geometry(root_geom)
		try:
			# Contents Window
			contents_x = contents.winfo_x() + x
			contents_y = contents.winfo_y() + y
			contents_geom = f"+{contents_x}+{contents_y}"
			contents.geometry(contents_geom)

			# Create Window
			create_x = create.winfo_x() + x
			create_y = create.winfo_y() + y
			create_geom = f"+{create_x}+{create_y}"
			create.geometry(create_geom)
		except:
			pass

	window = tkinter.Toplevel(root)
	window.geometry(f"350x250+{root.winfo_x()+300}+{root.winfo_y()}")

	window.grid_columnconfigure(0, weight=1)
	window.grid_columnconfigure(1, weight=1)
	window.grid_rowconfigure(1, weight=1)

	create_button = ttk.Button(window, text='Create Flip', command=pop_up_input)
	create_button.grid(row=0, column=0, sticky='we')

	flip_delete_button = ttk.Button(window, text='Delete Flip', command=delete_flip)
	flip_delete_button.grid(row=0, column=1, sticky='we')

	flip_list = tkinter.Listbox(window, exportselection=False)
	flip_list.grid(row=1, column=0, columnspan=2, sticky='nwes')
	flip_list.config(font=('Tahoma', 12))

	flip_list.bind('<<ListboxSelect>>', on_select)

	window.bind('<Button-1>', save_click_position)
	window.bind('<B1-Motion>', window_dragging)

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
	root.focus_set()
	try:
		window.focus_set()
		try:
			contents.focus_set()
			create.focus_set()
		except:
			pass
	except:
		pass
	event.widget.focus_set()

def root_dragging(event):
	"""
	Updates display position from mouse drag

	event: tkinter event
	"""
	global click_x, click_y, window, contents, create
	x = event.x - click_x
	y = event.y - click_y
	new_x = root.winfo_x() + x
	new_y = root.winfo_y() + y
	new_geom = f"+{new_x}+{new_y}"
	root.geometry(new_geom)
	try:
		# Modify Window
		window_x = window.winfo_x() + x
		window_y = window.winfo_y() + y
		window_geom = f"+{window_x}+{window_y}"
		window.geometry(window_geom)
		try:
			# Contents Window
			contents_x = contents.winfo_x() + x
			contents_y = contents.winfo_y() + y
			contents_geom = f"+{contents_x}+{contents_y}"
			contents.geometry(contents_geom)

			# Create Window
			create_x = create.winfo_x() + x
			create_y = create.winfo_y() + y
			create_geom = f"+{create_x}+{create_y}"
			create.geometry(create_geom)
		except:
			pass
	except:
		pass

def flip_visualize():
	fv.visual_window(flips, root)

flips = fd.load_flips()

root = tkinter.Tk()
root.geometry("300x500")

# Sun Valley ttk theme
sv_ttk.set_theme("dark")
style = ttk.Style(root)
style.configure('title.TLabel', font=('Forte', 36))
style.configure('option.TButton', font=('Tahoma', 16))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=2)
root.grid_rowconfigure(3, weight=2)
#root.grid_columnconfigure(1, weight=1)

title_label = ttk.Label(text="TailFlip", style='title.TLabel')
title_label.grid(row=0)

button = ttk.Button(root, text="Open Flip", command=open_flip, style='option.TButton')
button.grid(row=1, sticky='nwes')

create_button = ttk.Button(root, text="Modify Flips", command=flip_customize_window, style='option.TButton')
create_button.grid(row=2, sticky='nwes')

visual_button = ttk.Button(root, text="Visualize Flips", command=flip_visualize, style='option.TButton')
visual_button.grid(row=3, sticky='nwes')

#root.overrideredirect(True)
root.bind('<Button-1>', save_click_position)
root.bind('<B1-Motion>', root_dragging)
root.mainloop() 