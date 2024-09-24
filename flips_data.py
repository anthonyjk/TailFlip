import os
from flip import Flip

folder = "Flips"

def download_flip(flip):
	if not os.path.exists(folder):
		os.makedirs(folder)

	flip_name = flip.get_name()+".json"

	file_path = os.path.join(folder, flip_name)

	flip.save_contents(file_path)

def load_flips():
	flip_data = {}

	if os.path.exists(folder):
		files = os.listdir(folder)
		for f in files:
			if '.json' in f:
				file_path = os.path.join(folder, f)
				read = open(file_path, "r", encoding='utf-8')
				card = read.read().split('\n')

				flip_data[f[:-5]] = Flip(f[:-5])
				for c in card:
					if len(c) > 0:
						flip_data[f[:-5]].add_card(c.split(" : "))
	return flip_data

def delete_file(flip_name):
	name = flip_name + '.json'
	if os.path.exists(folder):
		file_path = os.path.join(folder, name)
		try:
			os.remove(file_path)
		except:
			print("File does not exist.")

