import tkinter
from tkinter import *
from . import ChargepolFigure


class Properties_Window:
    def __init__(self):
        self.new = Toplevel()
        self.new.geometry("720x576")
        self.new.title("Properties")
        self.new.resizable = False

    def clear(self):
        self.new.destroy()


data = dict()


def configure(figure: ChargepolFigure.ChargepolFigure) -> dict:
    """
    Function will configure depending on the type of figure it is presented.
    :return:
    """
    global data
    done = tkinter.IntVar()

    prop_window = Properties_Window()
    master = prop_window.new

    dtitle_label = Label(master, text="Title of plot: ")
    dtitle_label.grid(row=0, column=0)

    dxlabel_label = Label(master, text="X-label: ")
    dxlabel_label.grid(row=1, column=0)

    dylabel_label = Label(master, text="Y-label: ")
    dylabel_label.grid(row=2, column=0)

    dtime_label = Label(master, text="Initial time: ")
    dtime_label.grid(row=3, column=0)

    dinterval_label = Label(master, text="Time interval: ")
    dinterval_label.grid(row=4, column=0)

    # Entries
    dtitle_entry = Entry(master)
    dtitle_entry.insert(0, f"{figure.sup_title}")
    dtitle_entry.grid(row=0, column=1)

    dxlabel_entry = Entry(master)
    dxlabel_entry.insert(0, f"{figure.x_label}")
    dxlabel_entry.grid(row=1, column=1)

    dylabel_entry = Entry(master)
    dylabel_entry.insert(0, f"{figure.y_label}")
    dylabel_entry.grid(row=2, column=1)

    dtime_entry = Entry(master)
    dtime_entry.insert(0, f"{figure.initial_time}")
    dtime_entry.grid(row=3, column=1)

    dinterval_entry = Entry(master)
    dinterval_entry.insert(0, f"{figure.time_interval}")
    dinterval_entry.grid(row=4, column=1)

    def get_info():
        global data
        data = {
            'Title': dtitle_entry.get(),
            'Init_Time': dtime_entry.get(),
            'Interval': dinterval_entry.get(),
            'Xlabel': dxlabel_entry.get(),
            'Ylabel': dylabel_entry.get(),
        }
        done.set(1)

    # Button
    submit = Button(master, text="Submit", command=get_info)
    submit.grid(row=5, column=1, columnspan=2)

    submit.wait_variable(done)
    prop_window.clear()

    return data
