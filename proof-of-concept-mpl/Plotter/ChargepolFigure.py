from enum import Enum
import tkinter
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter.messagebox as messagebox
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.gridspec import GridSpec
import pickle
import os.path
from math import sqrt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shapereader
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

# TODO: Create dynamic plots.
# TODO: Be able to reupload a .pickle file containing all the information from a ChargepolFigure plot.


TEXAS_COUNTIES = "Dependencies/Texas_County_Boundaries_Detailed/County.shp"

class FigureType(Enum):
    """
    FigureType is an enumeration subtype that contains symbolic names for the type of figures we want to plot.
    """
    DENSITY         = 0
    HISTOGRAM       = 1
    SCATTER_PLOT    = 2
    HMAP            = 3


class ChargepolFigure:
    """
    ChargepolFigure is the main class that encapsulates all functions and attributes for any figure presented
    in the application. It (will) contain various functions that allow us to easily plot such figures in the application.
    As well as to get useful information about the plot and the ability to modify such plots in run-time.
    """
    def __init__(self, filepath, master: Frame, type_fig: FigureType):
        self.filep = filepath
        self.chargepol_data = self.process_chargepol()
        #print(self.chargepol_data["Timestamp"])
        if self.chargepol_data is None:
            return

        self.type = type_fig

        self.master_widget = master

        self.canvas, self.toolbar = None, None

        data = self.getInfo()
        self.sup_title = data['Title']
        self.initial_time = data['Init_Time']
        self.time_interval = data['Interval']
        self.x_label = data['Xlabel']
        self.y_label = data['Ylabel']

        # Verifying if info is good.
        if self.initial_time == '':
            self.initial_time = 0
        else:
            self.initial_time = float(self.initial_time)

        if self.time_interval == '':
            self.time_interval = 0
        else:
            self.time_interval = float(self.time_interval)

        # Determining type of figure.
        if data['Figure_Type'] == "Density":
            self.type = FigureType.DENSITY
        elif data['Figure_Type'] == "Histogram":
            self.type = FigureType.HISTOGRAM
        elif data['Figure_Type'] == "Scatter":
            self.type = FigureType.SCATTER_PLOT
        elif data['Figure_Type'] == "Houston Map":
            self.type = FigureType.HMAP
        else:
            raise RuntimeError("Invalid figure type.")


        # figure ax duo will contain all the information of the matplotlib plot itself.
        self.fig, self.ax = plt.subplots()

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
            return None

        res = {
            "Timestamp": chargepol_data['time'].tolist(), # Time of event
            "Charge"   : [chargepol_data['charge'].tolist(), chargepol_data['zmin'].tolist(), chargepol_data['zwidth'].tolist()], # Type of charge.
            "Location" : [chargepol_data['lon'].tolist(), chargepol_data['lat'].tolist()]# Longitude and latitude.
        }

        self.dateList = list()
        for i, n in enumerate(self.filep):
            self.dateList.append(self.filep[i][-8:-6] + "/" + self.filep[i][-6:-4])

        return res

    def verify_file(self) -> pd.DataFrame:
        """
        Verifies whether the given csv file (as of now) is a valid chargepol file. It does this by checking
        if the csv files has the correct number of columns (8) and the labels for each value are correct.
        :param:
        :return: A pandas dataframe containing all the chargepol data.
        """
        chargepol_labels = ['charge', 'time', 'zmin', 'zwidth', 'x', 'y', 'lon', 'lat']
        # Two things we check for chargepol. It has the correct number of rows (8) and the values are correct.
        # Creating dataframe to determine validity.
        dataframes = []
        for i, n in enumerate(self.filep):
            if self.filep[i].endswith('.csv'):
                #print(self.filep[i])
                df = pd.read_csv(self.filep[i], skiprows=[0, 1])  # We skip the main comments above.
                df['time'] = df['time'] + (86400 * i)
                dataframes.append(df)
            else:
                raise NotImplemented
            merged_df = pd.concat(dataframes, ignore_index=True)

        if merged_df.shape[1] != 8 or sorted(chargepol_labels) != sorted(merged_df.keys().array):
            messagebox.showerror("Invalid file", "Error: this csv file does not seem to be a valid Chargepol file.")
            return None

        return merged_df

    def createWidget(self) -> FigureCanvasTkAgg:
        """
        Creates the respective Figure Widget for the tkinter applicaiton.
        :return: Widget instance.
        """
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master_widget)
        self.canvas.draw()
        graph_display = self.canvas.get_tk_widget()
        graph_display.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        #
        # # Attempting to create toolbar.
        # toolbar = NavigationToolbar2Tk(self.canvas, window=self.master_widget)
        # toolbar.update()
        # toolbar.place(relx=0.5, rely=1, relwidth=1, anchor=S)

        return self.canvas

    def plot_data(self):
        # Utility inner function to determine time interval.
        def withinInterval(timePoint) -> bool:
            return self.initial_time < timePoint < (self.initial_time + self.time_interval)
        # Clearing previous data from axis.
        self.ax.clear()

        if self.type == FigureType.DENSITY:
            # TODO: Plot density plot
            time_points = list()
            for index, time in enumerate(self.chargepol_data['Timestamp']):
                if self.initial_time < time:
                    if (self.initial_time + self.time_interval) < self.chargepol_data['Timestamp'][index]: continue
                    charge = self.chargepol_data['Charge'][0][index]
                    # Plotting positive events.
                    if charge.strip() == "pos":
                        self.ax.plot([self.chargepol_data['Timestamp'][index], self.chargepol_data['Timestamp'][index] + .001],
                                [self.chargepol_data['Charge'][1][index], self.chargepol_data['Charge'][1][index] + self.chargepol_data['Charge'][2][index]],
                                color=[1, 0.062, 0.019], linewidth=1)
                    # Plotting negative events.
                    if charge.strip() == "neg":
                        self.ax.plot([self.chargepol_data['Timestamp'][index], self.chargepol_data['Timestamp'][index] + .001],
                                [self.chargepol_data['Charge'][1][index], self.chargepol_data['Charge'][1][index] + self.chargepol_data['Charge'][2][index]],
                                color=[0.062, 0.019, 1], linewidth=1)
                    time_points.append(time)

            # Error handling here check if timePoints is empty if so then throw error
            if not time_points:
                raise Exception("No lightning activity at the time chosen")

            # Plotting density
            ax1 = self.ax.twinx()
            density = gaussian_kde(time_points)
            density.covariance_factor = lambda: .25
            density._compute_covariance()
            xs = np.linspace(time_points[0], time_points[-1], len(time_points))
            ax1.plot(xs, density(xs), color=[0, 0, 0], marker=',')
            # Hiding y-axis values
            ax1.set_yticks([])
            if int(time_points[-1]) - int(time_points[0]) >= 172800:  # if our interval is greater or equal to 2 days
                 ticks = []
                 for i in range(int(time_points[0]), int(time_points[-1])):
                     if i % 86400 == 0:
                         ticks.append(i)
                 plt.xticks(ticks)
                 self.ax.figure.canvas.draw()
                 labels = [item.get_text() for item in self.ax.get_xticklabels()]
                 startingDateChargePol = int(self.initial_time / 86400)
                 endingDateChargePol = startingDateChargePol + len(ticks)
                 self.dateList = self.dateList[startingDateChargePol:endingDateChargePol]
                 #print(self.dateList)
                 for i, n in enumerate(self.dateList):
                     labels[i] = self.dateList[i]
                 self.ax.set_xticklabels(labels)

            self.ax.set(ylim=[0, 15])
            self.ax.set(xlabel=self.x_label, ylabel=self.y_label)
            self.ax.set_title(self.sup_title)
            plt.grid()

        elif self.type == FigureType.HISTOGRAM:
            posEventIntAlt = list()
            negEventIntAlt = list()

            for index, timePoint in enumerate(self.chargepol_data['Timestamp']):
                if self.initial_time < self.chargepol_data['Timestamp'][index]:
                    if (self.initial_time + self.time_interval) < self.chargepol_data['Timestamp'][index]: continue
                    charge = self.chargepol_data['Charge'][0][index]
                    if charge.strip() == "pos":
                        posEventIntAlt.append(self.chargepol_data['Charge'][1][index])
                    if charge.strip() == "neg":
                        negEventIntAlt.append(self.chargepol_data['Charge'][1][index])

            self.ax.hist(posEventIntAlt, bins=int(sqrt(len(posEventIntAlt))), density=True, color=[1, 0.062, 0.019, 0.7]
                    , orientation="horizontal")
            self.ax.hist(negEventIntAlt, bins=int(sqrt(len(negEventIntAlt))), density=True, color=[0.062, 0.019, 1, 0.7]
                    , orientation="horizontal")
            self.ax.set(ylabel=self.y_label, xlabel=self.x_label)
            self.ax.set_title(self.sup_title)

        elif self.type == FigureType.SCATTER_PLOT:
            negAlt = [[], []]  # Index 0 are all longitudes, index 1 are all latitudes
            posAlt = [[], []]
            time_points = list()

            for index, event in enumerate(self.chargepol_data['Charge'][0]):
                if event == 'pos' and withinInterval(self.chargepol_data["Timestamp"][index]):
                    posAlt[0].append(self.chargepol_data["Timestamp"][index])
                    posAlt[1].append(self.chargepol_data['Charge'][1][index])
                elif event == 'neg' and withinInterval(self.chargepol_data["Timestamp"][index]):
                    negAlt[0].append(self.chargepol_data["Timestamp"][index])
                    negAlt[1].append(self.chargepol_data['Charge'][1][index])
                time_points.append(self.chargepol_data["Timestamp"][index])

            # TODO: Let user choose whether a vertical or horizontal scatterplot.

            if int(time_points[-1]) - int(time_points[0]) >= 172800:  # if our interval is greater or equal to 2 days
                 ticks = []
                 for i in range(int(time_points[0]), int(time_points[-1])):
                     if i % 86400 == 0:
                         ticks.append(i)
                 plt.xticks(ticks)
                 self.ax.figure.canvas.draw()
                 labels = [item.get_text() for item in self.ax.get_xticklabels()]
                 startingDateChargePol = int(self.initial_time / 86400)
                 endingDateChargePol = startingDateChargePol + len(ticks)
                 self.dateList = self.dateList[startingDateChargePol:endingDateChargePol]
                 #print(self.dateList)
                 for i, n in enumerate(self.dateList):
                     labels[i] = self.dateList[i]
                 self.ax.set_xticklabels(labels)
                
            self.ax.scatter(x=negAlt[0], y=negAlt[1], s=10, linewidth=.625, color=[0.062, 0.019, 1], marker="_")
            self.ax.scatter(x=posAlt[0], y=posAlt[1], s=10, linewidth=.625, color=[1, 0.062, 0.019], marker="+")

            self.ax.set_title(self.sup_title)
            self.ax.set(ylabel=self.y_label, xlabel=self.x_label)

        elif self.type == FigureType.HMAP:
            negPos = [[], []]  # Index 0 are all longitudes, index 1 are all latitudes
            posPos = [[], []]

            for index, event in enumerate(self.chargepol_data['Charge'][0]):
                if event == 'pos' and withinInterval(self.chargepol_data["Timestamp"][index]):
                    posPos[0].append(float(self.chargepol_data['Location'][0][index]))
                    posPos[1].append(float(self.chargepol_data['Location'][1][index]))
                elif event == 'neg' and withinInterval(self.chargepol_data["Timestamp"][index]):
                    negPos[0].append(float(self.chargepol_data['Location'][0][index]))
                    negPos[1].append(float(self.chargepol_data['Location'][1][index]))

            # Removing pre-created axis.

            self.fig.get_axes()[0].set_axis_off()
            # Redefining self.ax to a cartopy-geosubaxes
            self.ax1 = self.fig.add_subplot(projection=ccrs.PlateCarree())


            county_lines = cfeature.ShapelyFeature(shapereader.Reader(TEXAS_COUNTIES).geometries(), ccrs.PlateCarree(),
                                                   facecolor='none', edgecolor='black', lw=1)
            self.ax1.add_feature(county_lines)

            # Zoom in on the Houston area by setting longitude/latitude parameters
            self.ax1.set_extent(
                [-98, -92, 28, 32],
                crs=ccrs.PlateCarree()
            )

            # , s=4, linewidth=.5, color=[1, 0.062, 0.019, .5]
            self.ax1.scatter(x=posPos[0], y=posPos[1], s=4, linewidth=.5, color=[1, 0.062, 0.019, .5],
                             marker='+', transform=ccrs.PlateCarree())

            # , s=4, linewidth=.5, color=[0.062, 0.019, 1, .5]
            self.ax1.scatter(x=negPos[0], y=negPos[1], s=4, linewidth=.5, color=[0.062, 0.019, 1, .5],
                             marker='_', transform=ccrs.PlateCarree())

            gl = self.ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
            gl.top_labels = False
            gl.right_labels = False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER

            self.ax1.set_title(self.sup_title)


    def getInfo(self) -> dict:
        """
        Creates a new widget window that allows the user to input all labels and titles for this instance figure.
        :return: Tuple containing all the information.
        """
        window = InfoWindow(self.chargepol_data)
        return window.data

    # See object serialization for this file.
    def store_file(self, filepath: str):
        # Creating pickle folder.
        # Redrawing plot.
        print(self.fig.get_axes())

        parent_dir = filepath.split('/')[:-1]
        parent_dir.append("Saved_files")
        pickle_path = "/".join(parent_dir)
        pickle_filename = filepath.split('/')[-1].split('.')[0]

        if not os.path.exists(pickle_path) or not os.path.isdir(pickle_path):
            os.mkdir(pickle_path)

        # Original file ::

        pickle_file = open(pickle_path + "/" + pickle_filename + ".pickle", 'wb')
        pickle.dump((self.fig, self.fig.get_axes()), pickle_file)
        pickle_file.close()

        plt.savefig(filepath)
        plt.savefig(pickle_path + "/" + pickle_filename + ".png")
class InfoWindow:
    def __init__(self, Chargepol):

        self.new = Toplevel()
        self.new.geometry("720x576")
        self.new.title("Information")
        self.new.resizable = False

        self.data = dict()

        self.done = IntVar()
        begintime = round(Chargepol['Timestamp'][0])
        endtime = round(Chargepol['Timestamp'][-1])
        intervalrange = "Interval is from", begintime, "to", endtime, "seconds."
        # Labels.

        self.figure_type_label = Label(self.new, text="Select type of figure").grid(row=0, column=1, pady=2)
        self.title_label = Label(self.new, text="Title").grid(row=1,column=1, pady=2)
        self.init_time_label = Label(self.new, text="Initial time").grid(row=2, column=1, pady=2)
        self.interval_range = Label(self.new, text=intervalrange).grid(row=2, column=3, pady=2)
        self.interval_time_label = Label(self.new, text="Time interval").grid(row=3, column=1, pady=2)
        self.xlabel_label = Label(self.new, text="X-label").grid(row=4, column=0, pady=2)
        self.ylabel_label = Label(self.new, text="Y-label").grid(row=4, column=2, pady=2)


        # Entries
        options = ["Density", "Histogram", "Scatter", "Houston Map"]
        dropdown_res = tkinter.StringVar(self.new)
        dropdown_res.set("Select an Option")
        self.figure_type_dropdown = OptionMenu(self.new, dropdown_res, *options)
        self.figure_type_dropdown.grid(row=0, column=2, pady=2, sticky='news')

        self.title_entry = Entry(self.new)
        self.title_entry.grid(row=1, column=2, pady=2, sticky='news')

        self.init_time_entry = Entry(self.new)
        self.init_time_entry.grid(row=2, column=2, pady=2, sticky='news')

        self.interval_time_entry = Entry(self.new)
        self.interval_time_entry.grid(row=3, column=2, pady=2, sticky='news')

        self.xlabel_entry = Entry(self.new)
        self.xlabel_entry.grid(row=4, column=1, pady=2, sticky='news')

        self.ylabel_entry = Entry(self.new)
        self.ylabel_entry.grid(row=4, column=3, pady=2, sticky='news')

        def get_info():
            self.data = {
                'Title': self.title_entry.get(),
                'Init_Time': self.init_time_entry.get(),
                'Interval': self.interval_time_entry.get(),
                'Xlabel': self.xlabel_entry.get(),
                'Ylabel': self.ylabel_entry.get(),
                'Figure_Type': dropdown_res.get()
            }
            self.done.set(1)

        # Button
        self.submit = Button(self.new, text="Submit", command=get_info)
        self.submit.grid(row=5, column=1, columnspan=2)

        self.submit.wait_variable(self.done)
        self.new.destroy()
