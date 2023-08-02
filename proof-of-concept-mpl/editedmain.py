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
import os
import pickle

# Other scripts in project
import Data_loader as DL
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

# TODO: Find where to store the static file SAVEDFILES

SAVED_FILES_PATH = "Saved_files/"

class App():
    def __init__(self, master):
        self.master = master
        self.master.grid()
        self.master.geometry("1280x720")
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

        # This empty list will parse and store all ChargepolFigures found in Saved_Files
        self.chargepolfigure_objects = dict()
        self.saved_data = dict()
        self.saved_figures = dict()
        self.buttonimages = dict()
        self.load_all_figures()
        self.generate_objects()

        # Initializing window where graph will live.
        self.graph_window = Frame(self.display_window, background='#536878')
        self.graph_window.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=CENTER)

        #! Uncomment when done with unpickling

        # img = Image.open('Saved_files/densityplot.png')
        # resized_image = img.resize((100, 100), Image.LANCZOS)
        #
        # self.click_btn = ImageTk.PhotoImage(resized_image)
        #
        # # img_label = Label(image=self.click_btn)
        #
        # self.my_button = Button(root, image=self.click_btn, command=self.update_image, justify=LEFT)

        # self.my_button.place(x=7, y=50)
        #
        # self.reload_file()

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
            self.graph.get_tk_widget().bind('<Button-1>', do_popup)

        selected = IntVar()
        menu = Menu(self.graph.get_tk_widget(), tearoff=0)
        menu.add_command(label="Properties", command=update_plot)
        menu.add_separator()
        menu.add_command(label="Save")
        menu.add_command(label="Save as...", command=save_file)

        # Main Loop after widget is created.

        self.graph.get_tk_widget().bind('<Button-3>', do_popup)
        menu.wait_variable(selected)

    def upload_file(self):
        # path = askdirectory(initialdir=',')
        # print(path)

        filename = filedialog.askopenfilenames(initialdir='.', filetypes=[
            ('Chargepol file', '.csv'),
            ('HDF5 file', '.h5')
        ])
        print(filename)
        data_loader = DL.DataLoader(self.graph_window, filename[0])
        if data_loader.chargepol_data is None:
            return
        self.plot_graph(data_loader.Cfigure)

    def update_image(self):
        # new_image = Image.open('Saved_files/217resistance.png')
        # resized_image = new_image.resize((100, 100), Image.LANCZOS)
        # self.click_btn = ImageTk.PhotoImage(resized_image)
        # self.my_button.image = new_image
        # self.my_button = Button(root, image=self.click_btn, command=self.update_image, justify=LEFT)

        # self.my_button.place(x=7, y=50)

        # img = Image.open('Saved_files/217resistance.png')
        # resized_image = img.resize((100, 100), Image.LANCZOS)
        #
        # self.click_btn = ImageTk.PhotoImage(resized_image)
        pass

    def load_all_figures(self):
        """Loads all figures found in the static saved_files file"""
        global SAVED_FILES_PATH
        for filename in os.listdir(SAVED_FILES_PATH):
            if SAVED_FILES_PATH + filename.split(".")[0] not in self.saved_figures:
                self.saved_figures[SAVED_FILES_PATH + filename.split(".")[0]] = [os.path.join(SAVED_FILES_PATH, filename)]
            else:
                self.saved_figures[SAVED_FILES_PATH + filename.split(".")[0]].append(os.path.join(SAVED_FILES_PATH, filename))

        # Create all ChargepolFigure Objects. Remember pickle file contains all the essential information about the file.
        for name, contents in self.saved_figures.items():
            pickle_file = ""
            for file in contents:
                if '.pickle' in file:
                    pickle_file = file

            with open(pickle_file, 'rb') as active_file:
                figure_data = pickle.load(active_file)
                self.saved_data[name] = figure_data

    def generate_objects(self):
        """Generates the respective chargepol_figure objects"""

        def create_image(master:Frame, filename:str, w, h, iteration):
            #print(filename)
            load = Image.open(fp=filename)
            self.buttonimages[iteration] = filename
            resized_load = load.resize((w, h), Image.LANCZOS)
            render = ImageTk.PhotoImage(resized_load)

            img = Button(master=master, image=render, command=lambda num=iteration: self.move_to_display(num), justify=LEFT)
            img.image = render
            img.place(relx=0, rely=0, relheight=1, relwidth=1)


        relx = 0.5; rely = 0.05
        width = 0.5
        iteration = 1
        for name, data in self.saved_data.items():
            new_frame = Frame(master=self.option_window, pady=20)
            new_frame.place(relx=relx, rely=rely, relwidth=width, relheight=0.15, anchor=N)

            new_object = ChargepolFigure.ChargepolFigure(None, new_frame, None,
                                                         load_from_file=True, saved_obj=data)

            new_frame.update()
            create_image(new_frame, name+".png", new_frame.winfo_width(), new_frame.winfo_height(), iteration)

            self.chargepolfigure_objects[name] = new_object

            rely += 0.15
            name = name[12:] + ".png"
            caption = Label(master=self.option_window, background='#323f4a', foreground='white', font=20,
                                     text=name)

            caption.place(relx=0.5, rely=rely, anchor=N)
            rely += 0.10
            iteration += 1

    def move_to_display(self, iteration):
        filename = self.buttonimages[iteration]
        #print(filename[:-4])
        figure = self.chargepolfigure_objects[filename[:-4]]
        figure.master_widget = self.graph_window
        self.plot_graph(figure)

        #raise NotImplemented


root = Tk()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        plt.close()
        quit()

app = App(root)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

