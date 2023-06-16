import matplotlib.pyplot as plt
import pickle

with open('Test.pickle', 'rb') as file:
    pickle.load(file)
    plt.savefig("Test.png")
