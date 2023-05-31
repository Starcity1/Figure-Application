# Auhtor : David Rodriguez Sanchez
# Proof of concept - Showcasing how to select and plot a certain graph to main display.

from tkinter import *
# from PIL import ImageTk,Image
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# from math import sqrt

# Matplotlib backend for canvas
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure


class App:
    def __init__(self, master):
        master.grid()
        master.geometry("1280x720")
        root.title("Proof of concept. Interactive matplotlib")

        # Frame 1 styling.
        self.option_window = LabelFrame(master, bg='#323f4a', borderwidth=0, width=master.winfo_screenwidth() / 5,
                                        height=master.winfo_screenheight())
        self.option_window.grid(row=0, column=0)

        self.option_text = Label(self.option_window, background='#323f4a', foreground='white', font=10, text="Options")
        self.option_text.place(relx=0.5, rely=0, anchor=N)
        # option_text.grid(row=0, column=0, pady=5, sticky='N')

        self.display_window = LabelFrame(master, bg='#536878', borderwidth=0,
                                         width=master.winfo_screenwidth() * (4 / 5),
                                         height=master.winfo_screenheight())
        self.display_window.grid(row=0, column=1)

        self.display_frame = Label(self.display_window, background='#536878', foreground='white', font=10,
                                   text="Display")
        self.display_frame.place(relx=0.5, rely=0, anchor=N)

        master.columnconfigure(1, weight=4)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)


root = Tk()
app = App(root)
root.mainloop()
