import sys
from data_types import *
from load_data import get_series
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

file_path = sys.argv[1]
series = get_series(file_path)



no_frames = len(series.sweeps)

sweep = series.sweeps[0]

xpoints = []
ypoints = []

for p in sweep.points:
    xpoints.append(p.x)
    ypoints.append(p.y)
    print(p)

fig, ax = plt.subplots()

all_scatter_plot = ax.scatter(xpoints, ypoints, s=10)
com_scatter_plot = ax.scatter(xpoints, ypoints, s=1)

def update(frame):
    sweep = series.sweeps[frame]
    xpoints = []
    ypoints = []
    for p in sweep.points:
        xpoints.append(p.x)
        ypoints.append(p.y)
    data = np.stack([xpoints, ypoints]).T
    all_scatter_plot.set_offsets(data)
    com_scatter_plot.set_offsets(data)

    return all_scatter_plot, com_scatter_plot

time_between_frames_ms = 40

ani = animation.FuncAnimation(fig=fig, func=update, frames=no_frames, interval=time_between_frames_ms)
plt.show()