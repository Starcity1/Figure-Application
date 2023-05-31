# Script creates a class that contains all information and functions for a function.

import matplotlib as mpl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt

class tk_figure:
    def __init__(self, x, y=None, ax=None, fig_type=""):
        self.fig = mpl.figure.Figure(figsize=(5, 4), dpi=100)
