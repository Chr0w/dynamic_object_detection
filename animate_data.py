import sys
from data_types import *
from load_data import get_series
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

series = get_series(sys.argv[1])
no_frames = len(series.sweeps)

sweep = series.sweeps[0]

xpoints = []
ypoints = []

for p in sweep.points:
    xpoints.append(p.x)
    ypoints.append(p.y)
    print(p)

fig, ax = plt.subplots()

scatter_plot = ax.scatter(xpoints, ypoints, s=1)

def update(frame):
    sweep = series.sweeps[frame]
    xpoints = []
    ypoints = []
    for p in sweep.points:
        xpoints.append(p.x)
        ypoints.append(p.y)
    print(p)
    data = np.stack([xpoints, ypoints]).T
    scatter_plot.set_offsets(data)

    return scatter_plot

ani = animation.FuncAnimation(fig=fig, func=update, frames=no_frames, interval=40)
plt.show()