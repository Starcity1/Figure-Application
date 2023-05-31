# Module imports
from tkinter import *
# from PIL import ImageTk,Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

# Matplotlib backend for canvas
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

# Dictionary holds all event ids.
EVENTS = {
    "LEFT":  mpl.backend_bases.MouseButton.LEFT,
    "RIGHT": mpl.backend_bases.MouseButton.RIGHT
}

class App():
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

        self.display_window = LabelFrame(master, bg='#536878', borderwidth=0, width=master.winfo_screenwidth() * (4 / 5),
                                         height=master.winfo_screenheight())
        self.display_window.grid(row=0, column=1)

        self.display_frame = Label(self.display_window, background='#536878', foreground='white', font=10, text="Display")
        self.display_frame.place(relx=0.5, rely=0, anchor=N)

        master.columnconfigure(1, weight=4)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.plot_graph()

    def plot_graph(self):

        data_example = np.random.normal(500, 40, 1000)
        self.fig = mpl.figure.Figure(figsize=(5, 4), dpi=100)

        # self.fig.canvas.mpl_connect('button_press_event', self.plot_zoom_in)
        # self.fig.canvas.mpl_connect('button_press_event', self.plot_zoom_out)

        # Manula zoom in and zoom out
        graph_window = Frame(self.display_window)
        graph_window.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=CENTER)


        self.ax = self.fig.subplots()
        self.ax.hist(data_example, int(sqrt(data_example.size)))
        self.ax.grid()
        # creating the Tkinter canvas containing the Matplotlib figure

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_window)
        self.canvas.draw()
        graph_display = self.canvas.get_tk_widget()
        graph_display.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        #
        # # Attempting to create toolbar.
        toolbar = NavigationToolbar2Tk(self.canvas, window=graph_window)
        toolbar.update()
        toolbar.place(relx=0.5, rely=1, relwidth=1, anchor=S)

    def plot_zoom_in(self, event):
        if event.button == EVENTS["LEFT"]:
            # print(f"plot_zoom_in detecting {EVENTS['LEFT']}.")
            # print(f"Mouse position :: x: {event.xdata}; y: {event.ydata}")
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()

            x_dist = ((x_max - x_min) / 2)
            y_dist = ((y_max - y_min) / 2)

            print(x_min, x_max)

            self.ax.set_xlim((event.xdata - x_dist) * .95, (event.xdata + x_dist) * .95)
            self.ax.set_ylim((event.ydata - y_dist) * .95, (event.ydata + y_dist) * .95)

            self.canvas.draw()

    def plot_zoom_out(self, event):
        if event.button == EVENTS["RIGHT"]:
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()

            x_dist = ((x_max - x_min) / 2)
            y_dist = ((y_max - y_min) / 2)

            print(x_min, x_max)

            self.ax.set_xlim((event.xdata - x_dist) * 1.05, (event.xdata + x_dist) * 1.05)
            self.ax.set_ylim((event.ydata - y_dist) * 1.05, (event.ydata + y_dist) * 1.05)

            self.canvas.draw()


root = Tk()
app = App(root)
root.mainloop()

