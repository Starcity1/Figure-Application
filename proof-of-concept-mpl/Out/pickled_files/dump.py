import matplotlib.pyplot as plt
import numpy as np
import pickle

data = np.linspace(0, 10, num=50)
y = np.cos(data)

fig, ax = plt.subplots()
ax.plot(data, y)

pickle.dump((fig, ax), open("Test.pickle", 'wb'))
