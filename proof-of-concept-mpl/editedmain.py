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
from tkinter.filedialog import askdirectory

# Other scripts in project
from Plotter import ChargepolFigure
from Plotter import Properties

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


        # Initializing window where graph will live.
        self.graph_window = Frame(self.display_window, background='#536878')
        self.graph_window.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=CENTER)

        img = Image.open('Saved_files/densityplot.png')
        resized_image = img.resize((100, 100), Image.LANCZOS)

        self.click_btn = ImageTk.PhotoImage(resized_image)

        # img_label = Label(image=self.click_btn)

        self.my_button = Button(root, image=self.click_btn, command=self.update_image, justify=LEFT)

        self.my_button.place(x=7, y=50)

        self.reload_file()

        buttonUploadFile = tkinter.Button(root, height=1, width=3, bg='green', command=self.upload_file)
        buttonUploadFile.place(x=1239, y=8)

    def plot_graph(self, figure: ChargepolFigure.ChargepolFigure):
        # Manula zoom in and zoom out
        figure.plot_data()
        self.graph = figure.createWidget()

        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
                selected.set(1)

        def save_file():
            f = filedialog.asksaveasfile(initialfile="Untitled.png", defaultextension=".png",
                                         filetypes=[("Image Documents", "*.png")])
            self.update_image() #updates button image

            figure.store_file(f.name)

        def update_plot():
            data = Properties.configure(figure)
            figure.sup_title = data['Title']
            figure.x_label = data['Xlabel']
            figure.y_label = data['Ylabel']
            figure.initial_time = float(data['Init_Time'])
            figure.time_interval = float(data['Interval'])

            # Verifying if info is good.
            if figure.initial_time == '':
                figure.initial_time = 0
            else:
                figure.initial_time = float(figure.initial_time)

            if figure.time_interval == '':
                figure.time_interval = 0
            else:
                figure.time_interval = float(figure.time_interval)

            self.graph = figure.update_plot()
            self.graph.get_tk_widget().bind('<Button-3>', do_popup)

        selected = IntVar()
        menu = Menu(self.graph.get_tk_widget(), tearoff=0)
        menu.add_command(label="Properties", command=update_plot)
        menu.add_separator()
        menu.add_command(label="Save")
        menu.add_command(label="Save as...", command=save_file)

        # Main Loop after widget is created.

        # TODO: Figure Out why popup menu can only be clicked once.

        self.graph.get_tk_widget().bind('<Button-3>', do_popup)
        menu.wait_variable(selected)

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
        # path = askdirectory(initialdir=',')
        # print(path)

        filename = filedialog.askopenfilenames(initialdir='.',
                                             filetypes=[('Chargepol files', '*.csv'), ('HLMA raw', '*.hdf5')])
        new_chargepol_figure = ChargepolFigure.ChargepolFigure(filename, self.graph_window,
                                                               ChargepolFigure.FigureType.DENSITY)
        if new_chargepol_figure.chargepol_data is None:
            return
        self.plot_graph(new_chargepol_figure)


    def update_image(self):
        new_image = Image.open('Saved_files/217resistance.png')
        resized_image = new_image.resize((100, 100), Image.LANCZOS)
        self.click_btn = ImageTk.PhotoImage(resized_image)
        self.my_button.image = new_image
        self.my_button = Button(root, image=self.click_btn, command=self.update_image, justify=LEFT)

        self.my_button.place(x=7, y=50)

        # img = Image.open('Saved_files/217resistance.png')
        # resized_image = img.resize((100, 100), Image.LANCZOS)
        #
        # self.click_btn = ImageTk.PhotoImage(resized_image)
    def reload_file(self):
        pass




root = Tk()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        plt.close()
        quit()

app = App(root)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

