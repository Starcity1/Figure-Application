# Data_loader.py : Part of the dependency for this entire script! DO NOT DELETE!!!

# -- Libraries
import tkinter

import numpy as np
import tkinter.messagebox as messagebox
from enum import Enum
import os


# -- Scripts
from Dependencies.Chargepol import chargepol
from Plotter import ChargepolFigure as CFig

"""
The intention of this code is for the application to load different types of files
to the application. For now only chargepol files and .hdf5 files are supported. Maybe raw ASCII files will be added
later. 

See draw.io diagram to understand the relationships and uses for each file.
"""


class FileType(Enum):
    UNDEFINED = "FileType.UNDEFINED"
    CHARGEPOL = "FileType.CHARGEPOL"
    HDF5 = "FileType.HDF5"



class DataLoader:
    # Init will allow us to determine and create a chargepol figure from an hdf5 file.
    def __init__(self, master: tkinter.Frame, file: str):
        self.CFigure = None

        self.file = file
        self._file_splitted = self.file.split('.')
        self.file_type = self._determine_file()

        # If file implemented was invalid we simply create a popup that tells the user so.
        if self.file_type == FileType.UNDEFINED:
            messagebox.showerror(title="Invalid File", message="ERROR: An invalid format was provided.")
            return

        self.Cfigure = self._process_file()



    def _determine_file(self) -> FileType:
        extension = self._file_splitted[-1]
        # All the machinery to process our Chargepol file is stored in ChargepolFigure.py. So we will just return the
        # CHARGEPOL enum
        match(extension):
            case 'csv':
                return FileType.CHARGEPOL
            case 'hdf5':
                return FileType.HDF5
            case _:
                return FileType.UNDEFINED


    def _process_file(self) -> CFig.ChargepolFigure:
        # If we have a Chargepol Figure then we can simply create a CFigure.
        if self.file_type is FileType.CHARGEPOL:
            # Create ChargepolFigure.
            raise NotImplemented
        elif self.file_type is FileType.HDF5:
            # Create the window popup to set up the values for chargepol, then create
            # Chargepol Figure.
            hdf5win = WindowHandler(self)

    def hdf5Poppup(self):
        pass



# TODO: Check if we need to implement a Window Handler for the Chargepol data.
"""
Class WindowHandler -

For now, it will only handle hdf5 files, but maybe in the future an implementation for
raw ASCII data files may come up. 

WindowHandler is an enclosing class. The classes in WindowHandler will contains
the specific windows for each type of file. WindowHandler will also get all the logic to determine
Which window the program should display.
"""
class WindowHandler:
    """ Init contains all the logic to determine which window we should output."""
    def __init__(self, loader: DataLoader):
        self.user_input = None
        match(loader.file_type):
            case FileType.HDF5:
                # Line initializes and outputs window
                hdf5win = self.HDF5Window()
                # Second line saves user's input data.
                self.user_input = hdf5win.data


    class HDF5Window:
        def __init__(self, master):
            self.data = dict()
            new_window = tkinter.Toplevel()
            new_window.geometry("720x576")
            new_window.title("Information")


        def _get_data(self):
            pass

# MAIN FUNCTION USED FOR TESTING ONLY! DO NOT USE FOR ETNIRE PROGRAM
if __name__ == "__main__":
    PATH = "./Example_data/happy_path_chargepol.csv"
    root = tkinter.Tk()
    root.geometry("1280x720")

    main_frame = tkinter.Frame(master=root)

    testInstnace = DataLoader(main_frame, PATH)
    root.quit()
