import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
from flip import Flip
import tkinter
from tkinter import ttk
import sv_ttk

matplotlib.use("TkAgg")

visual = None
def visual_window(flips, root):
	global visual
	sns.set_style('darkgrid')
	sns.set_palette('colorblind')
	visual = tkinter.Toplevel(root)

	flip_contents_graph(flips, root)

def flip_contents_graph(flips, root):
	"""
	Graphs the # of cards in each flip as a bargraph

	flips: dictonary object of Flip objects
	"""
	global visual

	fig, flip_plot = plt.subplots()
	fig.set_figwidth(3)
	fig.set_figheight(3)

	#fig.patch.set_facecolor('#3f4544')

	visual.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), visual.destroy()))
	root.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), root.destroy()))

	bar_contents = FigureCanvasTkAgg(fig, visual)
	bar_contents.get_tk_widget().grid()

	x = []
	y = []
	for f in flips:
		x.append(f)
		y.append(len(flips[f].get_cards()))

	fc_plot = sns.barplot(x=x, y=y, ax=flip_plot, hue=x, legend=False)
	fc_plot.tick_params(axis='x', labelrotation=45)
	fc_plot.set(xlabel="Flip", ylabel="Cards", title="Flips Card Amount")
	fig.tight_layout()