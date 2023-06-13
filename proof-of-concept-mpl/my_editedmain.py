# Module imports
import tkinter
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk,Image
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from tkinter import filedialog
import tkinter.messagebox as messagebox

# Other scripts in project
from Plotter import ChargepolFigure

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

        button1 = tkinter.Button(root, text="Density Graph")
        button1.place(x=7, y=50)

        button2 = tkinter.Button(root, text="Histogram")
        button2.place(x=7, y=80)

        button3 = tkinter.Button(root, text="Scatter Plot")
        button3.place(x=7, y=110)

        button4 = tkinter.Button(root, text="Event Layer on Houston")
        button4.place(x=7, y=140)

        button5 = tkinter.Button(root, text="Density Graph and Histogram")
        button5.place(x=7, y=170)

        button6 = tkinter.Button(root, text="Density Graph and Scatter Plot")
        button6.place(x=7, y=200)

        button7 = tkinter.Button(root, text="Density Graph and Scatter Plot with Map")
        button7.place(x=7, y=230)

        button8 = tkinter.Button(root, text="All Plots")
        button8.place(x=7, y=260)

        #img = Image.open('uploadsign.png')
        #img = img.resize((50, 50), Image.ANTIALIAS)
        #photo = ImageTk.PhotoImage(img)

        # Initializing window where graph will live.
        self.graph_window = Frame(self.display_window, background='#536878')
        self.graph_window.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=CENTER)

        #photo = ImageTk.PhotoImage(Image.open("plus.gif"))
        buttonUploadFile = tkinter.Button(root, height=1, width=3, bg='green', command=self.upload_file)
        buttonUploadFile.place(x=1239, y=8)

    def plot_graph(self, figure: ChargepolFigure.ChargepolFigure):
        # Manula zoom in and zoom out
        figure.plot_data()
        graph = figure.createWidget()

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

    def upload_file(self):
        filename = filedialog.askopenfilename(initialdir='.',
                                              filetypes=[('Chargepol files', '*.csv'), ('HLMA raw', '*.hdf5')])
        new_chargepol_figure = ChargepolFigure.ChargepolFigure(filename, self.graph_window,
                                                               ChargepolFigure.FigureType.DENSITY)
        if new_chargepol_figure.chargepol_data is None:
            return
        self.plot_graph(new_chargepol_figure)



root = Tk()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        quit()

app = App(root)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

