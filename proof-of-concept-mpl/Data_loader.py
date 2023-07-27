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

        self.chargepol_data = None
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
            # TODO: Increment the security for this file for more strange cases e.g: a file containing .csv files and other files.
            for indiv_file in os.listdir(self.file):
                indiv_extension = indiv_file.split('.')[-1]
                match indiv_extension:
                    case 'csv':
                        return FileType.CHARGEPOL
                    case 'h5':
                        return FileType.HDF5

        return FileType.UNDEFINED


    def _process_file(self) -> CFig.ChargepolFigure:
        # If we have a Chargepol Figure then we skip and create a figure in editedmain.py as usual
        if self.file_type is FileType.CHARGEPOL:
            self.Cfigure = CFig.ChargepolFigure((self.file, ), self.master, CFig.FigureType.DENSITY)
        elif self.file_type is FileType.HDF5:
            # Create the window popup to set up the values for chargepol, then create
            # Chargepol Figure here.
            hdf5win = WindowHandler(self)

            # hdf5win.user_input will contain all of the user's input data.
            try:
                directory   = hdf5win.user_input['Dir_path']
                netw_ctr    = np.array([float(hdf5win.user_input['Latitude']), float(hdf5win.user_input['Longitude'])])
                max_r       = float(hdf5win.user_input['Max_range'])
                nsou        = float(hdf5win.user_input['Nsou'])
                self.chargepol_data = chargepol.init_chargepol(directory, netw_ctr, max_r, nsou)
                self.Cfigure = CFig.ChargepolFigure(None, self.master, CFig.FigureType.DENSITY, data_loader=self.chargepol_data)
            except Exception as e:
                messagebox.showerror(message="Error: Invalid information was provided. Aborting.")
                raise e



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
            new_window.geometry("480x620")
            new_window.title("Information")
            new_window.resizable(width=False, height=False)

            # Making the window sticky for all cases.
            new_window.rowconfigure('all', weight=1)
            new_window.columnconfigure('all', weight=1)

            row_itr = 0 # Will be constantly updated if we wish to introduce a new row within other rows.

            # Path Entry.
            self.directory_path_label = tkinter.Label(master=new_window, text="Path: ")
            self.directory_path_label.grid(row=row_itr, column=0, padx=5, pady=5)
            self.directory_strvar = tkinter.StringVar()
            self.directory_path_entry = tkinter.Entry(master=new_window, textvariable=self.directory_strvar)
            self.directory_strvar.set(self.loader.file)
            self.directory_path_entry.grid(row=row_itr, column=1, padx=5, pady=5)

            row_itr += 1

            # Longitude/Latitude Entries.
            self.network_center_label = tkinter.Label(master=new_window, text="Network's lon/lat")
            self.network_center_label.grid(row=row_itr, column=0, columnspan=2)
            row_itr += 1

            self.lon_strvar = tkinter.StringVar()
            self.longitude_label = tkinter.Label(master=new_window, text="Longitude: ")
            self.longitude_label.grid(row=row_itr, column=0, padx=5, pady=5)
            self.longitude_entry = tkinter.Entry(master=new_window, textvariable=self.lon_strvar)
            self.lon_strvar.set("-95.37") # Hard-coded the longitude of HLMA center
            self.longitude_entry.grid(row=row_itr, column=1, padx=5, pady=5)
            row_itr += 1

            self.lat_strvar = tkinter.StringVar()
            self.latitude_label = tkinter.Label(master=new_window, text="Latitude: ")
            self.latitude_label.grid(row=row_itr, column=0, padx=5, pady=5)
            self.latitude_entry = tkinter.Entry(master=new_window, textvariable=self.lat_strvar)
            self.lat_strvar.set("29.76") # Hard-coded the latitude of HLMA center
            self.latitude_entry.grid(row=row_itr, column=1, padx=5, pady=5)
            row_itr += 1

            # Max range entry
            self.max_range_label = tkinter.Label(master=new_window, text="Max Range (km): ")
            self.max_range_label.grid(row=row_itr, column=0, padx=5, pady=5)
            self.max_range_entry = tkinter.Entry(master=new_window)
            self.max_range_entry.grid(row=row_itr, column=1, padx=5, pady=5)
            row_itr += 1

            # Number of sources entry
            self.nsou_label = tkinter.Label(master=new_window, text="Number of sources: ")
            self.nsou_label.grid(row=row_itr, column=0, padx=5, pady=5)
            self.nsou_entry = tkinter.Entry(master=new_window)
            self.nsou_entry.grid(row=row_itr, column=1, padx=5, pady=5)
            row_itr += 1

            self.submit = tkinter.Button(new_window, text="Submit", command=self._get_data)
            self.submit.grid(row=row_itr, column=0, columnspan=2, padx=2, pady=2)

            while True:
                self.submit.wait_variable(self.done)
                if self.done.get() == 1:
                    break

                not_empty = messagebox.showerror(message="Error: Not all fields were filled.")
                self.done.set(0)

            new_window.destroy()

        def _get_data(self):
            # We first determine if all entries are filled
            entries = [
                self.directory_path_entry.get(),
                self.longitude_entry.get(),
                self.latitude_entry.get(),
                self.max_range_entry.get(),
                self.nsou_entry.get(),
            ]

            if not all(entries):
                self.done.set(2)
                return

            # If all are filled then we upload all data to our dictionary.
            self.data = {
                'Dir_path':     self.directory_path_entry.get(),
                'Longitude':    self.longitude_entry.get(),
                'Latitude':     self.latitude_entry.get(),
                'Max_range':    self.max_range_entry.get(),
                'Nsou':         self.nsou_entry.get(),
            }

            self.done.set(1)

# MAIN FUNCTION USED FOR TESTING ONLY! DO NOT USE FOR ENTIRE PROGRAM
if __name__ == "__main__":
    HDF5_PATH = "./Example_data/hdf5-files/2017/Aug/26/"
    CHARGEPOL_PATH = "./Example_data/happy_path_chargepol.csv"
    root = tkinter.Tk()
    root.geometry("1280x720")

    main_frame = tkinter.Frame(master=root)

    testInstnace = DataLoader(main_frame, CHARGEPOL_PATH)
    root.quit()
