# Figure Application
# Author : David Rodriguez Sanchez
# Version : 0.0.1
# Please, refer to the README.md found on the GitHub repository which contains all the information
# for this application.
# https://github.com/Starcity1/Figure-Application
#

# Module imports
from tkinter import *
from tkinter import ttk

# File imports
from main_window import window

def main():
    app = Tk()

    window.MainWindow(tk_instance=app)

    app.mainloop()


if __name__ == '__main__':
    main()
