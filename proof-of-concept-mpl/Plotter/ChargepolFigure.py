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

# TODO: Add the appropiate logic to determine a time interval and initial time.
# TODO: Create dynamic plots.
# TODO: Be able to reupload a .pickle file containing all the information from a ChargepolFigure plot.


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


        # figure ax duo will contain all the information of the matplotlib plot itself.
        self.fig, self.ax = plt.subplots()
        self.spec = GridSpec(nrows=4, ncols=4)

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
            print(self.filep[i])
            self.dateList.append(self.filep[i][-8:-6] + "/" + self.filep[i][-6:-4])

        print(self.dateList)
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
        # Clearing previous data from axis.
        self.ax.clear()

        if self.type == FigureType.DENSITY:
            # TODO: Plot density plot
            time_points = list()
            # print(list(enumerate(timeList)))
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

            # TODO: Implement logic to detect and plot multiple days.
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
            plt.suptitle(self.sup_title)
            plt.grid()
        elif self.type == FigureType.HISTOGRAM:
            # TODO: Plot histogram
            pass
        elif self.type == FigureType.SCATTER_PLOT:
            # TODO: Plot scatter_plot
            pass
        elif self.type == FigureType.HMAP:
            # TODO: Plot Houston Map
            pass

    def getInfo(self) -> dict:
        """
        Creates a new widget window that allows the user to input all labels and titles for this instance figure.
        :return: Tuple containing all the information.
        """
        window = InfoWindow()
        return window.data


class InfoWindow:
    def __init__(self):
        self.new = Toplevel()
        self.new.geometry("720x576")
        self.new.title("Information")
        self.new.resizable = False

        self.data = tuple()
        self.done = IntVar()

        # Labels.
        self.title_label = Label(self.new, text="Title").grid(row=0,column=1, pady=2)
        self.init_time_label = Label(self.new, text="Initial time").grid(row=1, column=1, pady=2)
        self.interval_time_label = Label(self.new, text="Time interval").grid(row=2, column=1, pady=2)
        self.xlabel_label = Label(self.new, text="X-label").grid(row=3, column=0, pady=2)
        self.ylabel_label = Label(self.new, text="Y-label").grid(row=3, column=2, pady=2)

        # Entries
        self.title_entry = Entry(self.new)
        self.title_entry.grid(row=0, column=2, pady=2)

        self.init_time_entry = Entry(self.new)
        self.init_time_entry.grid(row=1, column=2, pady=2)

        self.interval_time_entry = Entry(self.new)
        self.interval_time_entry.grid(row=2, column=2, pady=2)

        self.xlabel_entry = Entry(self.new)
        self.xlabel_entry.grid(row=3, column=1, pady=2)

        self.ylabel_entry = Entry(self.new)
        self.ylabel_entry.grid(row=3, column=3, pady=2)

        def get_info():
            self.data = {
                'Title': self.title_entry.get(),
                'Init_Time': self.init_time_entry.get(),
                'Interval': self.interval_time_entry.get(),
                'Xlabel': self.xlabel_entry.get(),
                'Ylabel': self.ylabel_entry.get(),
            }
            self.done.set(1)

        # Button
        self.submit = Button(self.new, text="Submit", command=get_info)
        self.submit.grid(row=4, column=1, columnspan=2)

        self.submit.wait_variable(self.done)
        self.new.destroy()
