from enum import Enum
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter.messagebox as messagebox
import pandas as pd

# TODO: Add the appropiate logic to determine a time interval and initial time.
# TODO: Create dynamic plots.
# TODO: Be able to reupload a .pickle file containing all the information from a ChargepolFigure plot.

class FigureType(Enum):
    """
    FigureType is an enumeration subtype that contains symbolic names for the type of figures we want to plot.
    """
    DENSITY = 0
    HISTOGRAM = 1
    SCATTER_PLOT = 2
    HMAP = 3


class ChargepolFigure:
    """
    ChargepolFigure is the main class that encapsulates all functions and attributes for any figure presented
    in the application. It (will) contain various functions that allow us to easily plot such figures in the application.
    As well as to get useful information about the plot and the ability to modify such plots in run-time.
    """
    def __init__(self, filepath, type : FigureType):
        self.filep = filepath
        self.chargepol_data = self.process_chargepol()
        self.type = type

        # figure ax duo will contain all the information of the matplotlib plot itself.
        self.fig, self.ax = plt.subplots()
        self.spec = mpl.gridspec.Gridspec(nrows=4, ncols=4)

    def process_chargepol(self) -> dict:
        """
        Within this object, we will generate a dictionary with the structure:
        dict :: {
            "Charge" : Charge column
            "Time"   : Time column
            "Zmin"   : Zmin column
            "Zwidth" : Zwidth column
            "X"      : X column
            "Y"      : Y column
            "Lon"    : Lon column
            "Lat"    : Lat column
        }
        :return: A dictionary with all the chargepol data ordered by time.
        """
        chargepol_data = self.verify_file()
        if chargepol_data is None:
            raise RuntimeError("No valid Chargepol file was given.")

        res = {
            "Charge" : [chargepol_data['charge']],
            "Time"   : [chargepol_data['time']],
            "Zmin"   : [chargepol_data['zmin']],
            "Zwidth" : [chargepol_data['zwidth']],
            "X"      : [chargepol_data['x']],
            "Y"      : [chargepol_data['y']],
            "Lon"    : [chargepol_data['lon']],
            "Lat"    : [chargepol_data['lat']]
        }

        return res

    def verify_file(self) -> pd.DataFrame:
        """
        Verifies the whether the given csv file (as of now) is a valid chargepol file. It does this by checking
        if the csv files has the correct number of columns (8) and the labels for each value are correct.
        :param:
        :return: A pandas dataframe containing all the chargepol data.
        """
        chargepol_labels = ['charge', 'time', 'zmin', 'zwidth', 'x', 'y', 'lon', 'lat']
        # Two things we check for chargepol. It has the correct number of rows (8) and the values are correct.
        # Creating dataframe to determine validity.
        if self.filep.endswith('.csv'):
            df = pd.read_csv(self.filep, skiprows=[0, 1])  # We skip the main comments above.
        else:
            raise NotImplemented

        if df.shape[1] != 8 or sorted(chargepol_labels) != sorted(df.keys().array):
            messagebox.showerror("Invalid file", "Error: this csv file does not seem to be a valid Chargepol file.")
            return None

        return df

    def plot_data(self):
        # Clearing previous data from axis.
        self.ax.clear()

        if self.type == FigureType.DENSITY:
            # TODO: Plot density plot
            pass
        elif self.type == FigureType.HISTOGRAM:
            # TODO: Plot histogram
            pass
        elif self.type == FigureType.SCATTER_PLOT:
            # TODO: Plot scatter_plot
            pass
        elif self.type == FigureType.HMAP:
            # TODO: Plot Houston Map
            pass
