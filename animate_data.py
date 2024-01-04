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

for p in sweep.all_points:
    xpoints.append(p.x)
    ypoints.append(p.y)

fig, ax = plt.subplots()

colors = ['blue', 'gold', 'chocolate', 'forestgreen', 'khaki', 'red', 'brown', 'cyan', 'firebrick',  'tomato', 'saddlebrown', 'peachpuff',  'yellow',   'lime', 'turquoise', 'blueviolet', 'violet', 'purple']
color_map = []
for c in sweep.all_points:
    color_map.append(colors[c.label])

all_scatter_plot = ax.scatter(xpoints, ypoints, s=10, c=color_map)
com_scatter_plot = ax.scatter(0, 0, s=40, c=color_map)


def update(frame):
    sweep = series.sweeps[frame]
    color_map = []
    for c in sweep.all_points:
        color_map.append(colors[c.label])
    xpoints = []
    ypoints = []
    for p in sweep.all_points:
        xpoints.append(p.x)
        ypoints.append(p.y)
    data = np.stack([xpoints, ypoints]).T
    all_scatter_plot.set_offsets(data)
    all_scatter_plot.set_facecolor(color_map)

    # x_com = []
    # y_com = []
    # for b in sweep.blobs:
    #     x_com.append(b.center_of_mass.x)
    #     y_com.append(b.center_of_mass.y)
        

    print(sweep.sec)

    return all_scatter_plot

time_between_frames_ms = 50

ani = animation.FuncAnimation(fig=fig, func=update, frames=no_frames, interval=time_between_frames_ms)
plt.show()