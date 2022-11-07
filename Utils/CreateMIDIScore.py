
import pypianoroll
import matplotlib.pyplot as plt

def create_score(path):
    multitrack = pypianoroll.read(path)
    multitrack.plot()
    #plt.show()
    plt.savefig('midiscore.png')
