import matplotlib.pyplot as plt
import pickle

with open('Saved_files/test.pickle', 'rb') as file:
    fig, axs = pickle.load(file)
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

    plt.savefig("pickled_test.png")
