# Module imports
from tkinter import *
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

# Matplotlib backend for canvas
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


def plot_graph():
    data_example = np.random.normal(500, 40, 1000)
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot().hist(data_example, int(sqrt(data_example.size)))
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=display_window)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=CENTER)


root = Tk()
root.title("Proof of concept. Interactive matplotlib")

root.grid()
root.geometry("1280x720")

# Frame 1 styling.
option_window = LabelFrame(root, bg='#323f4a', borderwidth=0, width=root.winfo_screenwidth()/5, height=root.winfo_screenheight())
option_window.grid(row=0, column=0)

option_text = Label(option_window, background='#323f4a', foreground='white', font=10, text="Options")
option_text.place(relx=0.5, rely=0, anchor=N)
# option_text.grid(row=0, column=0, pady=5, sticky='N')


display_window = LabelFrame(root, bg='#536878', borderwidth=0, width=root.winfo_screenwidth()*(4/5), height=root.winfo_screenheight())
display_window.grid(row=0, column=1)

display_frame = Label(display_window, background='#536878', foreground='white', font=10, text="Display")
display_frame.place(relx=0.5, rely=0, anchor=N)
# display_frame.grid(row=0, column=1, pady=5, sticky='N')
#Show graph.
plot_graph()

# Adding respective weights for resizing.
root.columnconfigure(1, weight=4)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()

