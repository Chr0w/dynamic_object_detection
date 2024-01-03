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

"""

scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
line2 = ax.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
ax.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    x = t[:frame]
    y = z[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(t[:frame])
    line2.set_ydata(z2[:frame])
    return (scat, line2)


ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
plt.show()

"""