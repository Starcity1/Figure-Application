from tkinter import *
from ChargepolFigure import ChargepolFigure, FigureType


class Properties_Window:
    def __init__(self):
        self.new = Toplevel()
        self.new.geometry("720x576")
        self.new.title("Information")
        self.new.resizable = False


def configure(figure: ChargepolFigure):
    """
    Function will configure depending on the type of figure it is presented.
    :return:
    """

    prop_window = Properties_Window()

    if figure.type == FigureType.DENSITY:
        # TODO: Allow user to reconfigure aspects of Density
        pass
    elif figure.type == FigureType.HISTOGRAM:
        # TODO: Allow user to reconfigure aspects of Histogram
        pass
    elif figure.type == FigureType.SCATTER_PLOT:
        # TODO: Allow user to reconfigure aspects of scatter plot.
        pass
    elif figure.type == FigureType.HMAP:
        # TODO: Allow user to reconfigure aspects of Houston map
        pass
