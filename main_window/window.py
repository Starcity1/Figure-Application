# Figure Application
# Author : David Rodriguez Sanchez
# Version : 0.0.1
# Please, refer to the README.md found on the GitHub repository which contains all the information
# for this application.
# https://github.com/Starcity1/Figure-Application
#

from tkinter import *
from tkinter import ttk


class MainWindow:
    """ class MainWindow - main class that manages display of the main window.

    The main window is divided into three main sections: Display frame, outline frame, figure preview frame.
    Each is represented as an inner, and initialized in the super constructor of MainWindow. Each inner class
    manages all operations and display execution for each section in the window. In addition, the file imports
    helper files for each section.

    Args:
        tkInstance - The instance of our tk application.
    """

    def __init__(self, tk_instance=Tk):
        self._master = tk_instance
        self._master.geometry("1366x768")
        self._master.title("Figure Generator")

        self._master.resizable(0, 0)
        self._master.columnconfigure(1, weight=3)
        self._master.columnconfigure(0, weight=1)

        self._master.rowconfigure(1, weight=1)
        self._master.rowconfigure(0, weight=3)

        self.height = self._master.winfo_screenheight()
        self.width  = self._master.winfo_screenwidth()

        print(f"height: {self.height}\nwidth: {self.width}")

        self.displayFrame(self._master)
        self.outlineFrame(self._master)
        self.figurePreviewFrame(self._master)

    # Main window, here the construction of the main figure will be showcased.
    class displayFrame:
        def __init__(self, tk_instance):
            print("Generating display")
            self.display = Frame(tk_instance).grid(row=0, column=1)
            self.display_label = Label(self.display, text="Label for Display!").grid(row=0, column=1)


    # Outline frame, here a selection of pre-made outlines for our figures will be showcased.
    # (e.g. XLMA file format, basic histogram, basic scatter plot, etc.)
    class outlineFrame:
        def __init__(self, tk_instance):
            print("Generating outline")
            self.outline = Frame(tk_instance, bg='red').grid(row=1, column=1)
            self.outline_label = Label(self.outline, text="Label for Outline!").grid(row=1, column=1)
    #
    class figurePreviewFrame:
        def __init__(self, tk_instance):
            print("Generating preview")
            self.preview = Frame(tk_instance).grid(row=0, column=0, rowspan=1)
            self.preview_label = Label(self.preview, text="Label for Preview!").grid(row=0, column=0, rowspan=1)
