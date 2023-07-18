# Data_loader.py : Part of the dependency for this entire script! DO NOT DELETE!!!

# -- Libraries
import numpy as np
import tkinter as tk
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
    UNDEFINED = -1
    CHARGEPOL = 0
    HDF5 = 1


class DataLoader:
    # Init will allow us to determine and create a chargepol figure from an hdf5 file.
    def __init__(self, file: str):
        self.CFigure = None

        self.file = file
        self._file_stripped = self.file.strip('.')
        self.file_type = determine_file()

        # If file implemented was invalid we simply create a popup that tells the user so.
        if self.file_type == FileType.UNDEFINED:
            # TODO: Raise popup
            pass

        self.Cfigure = self.process_file()



    def determine_file(self) -> FileType:
        extension = self._file_stripped[-1]
        # All the machinery to process our Chargepol file is stored in ChargepolFigure.py. So we will just return the
        # CHARGEPOL enum
        match(extension):
            case 'csv':
                return FileType.CHARGEPOL
            case 'hdf5':
                return FileType.HDF5
        return  FileType.UNDEFINED


    def process_file(self) -> CFig.ChargepolFigure:
        # If we have a Chargepol Figure then we can simply create a CFigure.
        pass

# TODO: Check if we need to implement a Window Handler for the Chargepol data.
class WindowHandler:
    pass