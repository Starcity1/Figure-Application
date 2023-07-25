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
        self.master = master
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

        # Two cases: We are handling a single file or multiple files.
        if os.path.isfile(self.file):
            match(extension):
                case 'csv':
                    return FileType.CHARGEPOL
                case 'h5':
                    return FileType.HDF5

        if os.path.isdir(self.file):
            # Check if at least one of the files is a .csv or .hdf5
            # TODO: Increment the security for this file for more strange cases
            # e.g: a file containing .csv files and other files.
            for indiv_file in os.listdir(self.file):
                indiv_extension = indiv_file.split('.')[-1]
                match indiv_extension:
                    case 'csv':
                        return FileType.CHARGEPOL
                    case 'h5':
                        return FileType.HDF5

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
        self.loader = loader
        match(loader.file_type):
            case FileType.HDF5:
                # Line initializes and outputs window
                hdf5win = self.HDF5Window(self)
                # Second line saves user's input data.
                self.user_input = hdf5win.data


    class HDF5Window:
        def __init__(self, windowInstance):
            self.loader = windowInstance.loader
            self.data = dict()
            self.done = tkinter.IntVar()
            new_window = tkinter.Toplevel(master=self.loader.master)
            new_window.geometry("720x576")
            new_window.title("Information")

            self.directory_path_label = tkinter.Label(master=new_window, text="Directory path: ")
            self.directory_path_label.grid(row=0, column=0, padx=5, pady=5)
            self.directory_strvar = tkinter.StringVar()
            self.directory_path_entry = tkinter.Entry(master=new_window,
                                                      textvariable=self.directory_strvar, state=tkinter.DISABLED)
            self.directory_strvar.set(self.loader.file)
            self.directory_path_entry.grid(row=0, column=1, padx=5, pady=5)

            def get_info():
                self.done.set(1)

            self.submit = tkinter.Button(new_window, text="Submit", command=get_info)
            self.submit.grid(row=1, column=1, sticky=tkinter.NSEW)
            self.submit.wait_variable(self.done)


        def _get_data(self):
            pass

# MAIN FUNCTION USED FOR TESTING ONLY! DO NOT USE FOR ETNIRE PROGRAM
if __name__ == "__main__":
    PATH = "./Example_data/hdf5-files/2017/Aug/26/"
    root = tkinter.Tk()
    root.geometry("1280x720")

    main_frame = tkinter.Frame(master=root)

    testInstnace = DataLoader(main_frame, PATH)
    root.quit()
