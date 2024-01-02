import sys
from dataclasses import dataclass
import math
from data_types import *


def get_front_scan_ranges(input_file):

    all_ranges = []
    front_scanner = False
    for line in input_file:
        if "front_laser_link" in line:
            front_scanner = True
        elif "back_laser_link" in line:
            front_scanner = False  

        if "secs" in line:
            time_stamp_seconds = [int(i) for i in line.split() if i.isdigit()]        

        if "nsecs" in line:
            time_stamp_nanoseconds = [int(i) for i in line.split() if i.isdigit()]

        if front_scanner and "ranges" in line:
            ranges_as_string = line[9:len(line)-2]
            ranges_as_list = list(ranges_as_string.split(", "))
            all_ranges.append(raw_sweep(ranges=ranges_as_list, sec= time_stamp_seconds[0], nsec=time_stamp_nanoseconds[0]))

    return all_ranges

def get_polar_coords_from_scan(data):

    angle_min = 2.3998663425445557
    angle_increment = -0.0029088794253766537
    
    all_polar_coord_list = []
    for sweep in data:
        sweep_polar_coords = []
        for i in range(0, len(sweep.ranges)):
            angle = angle_min + (angle_increment * i)
            dist = float(sweep.ranges[i])
            if dist < 12:
                sweep_polar_coords.append(PolarCoordinate(dist=dist, theta=angle))
        all_polar_coord_list.append(sweep_polar_coords)

    return all_polar_coord_list
    
def get_euclidian_coords(polar_coords):
    
    all_euclidian_coords = []

    for sweep in polar_coords:
        sweep_euclidian_coords = []

        for p in sweep:
            sweep_euclidian_coords.append(EuclidianCoordinate(x=math.cos(p.theta)*p.dist, y=math.sin(p.theta)*p.dist))
        
        all_euclidian_coords.append(sweep_euclidian_coords)

    return all_euclidian_coords

input_file_path = sys.argv[1]
output_file_path= sys.argv[2]
print(f"input_file: {input_file_path}")
print(f"output_file: {output_file_path}")

input_file = open(input_file_path, "r")

p = PolarCoordinate(0,0)

list_front_scan_ranges = get_front_scan_ranges(input_file)
polar_coords = get_polar_coords_from_scan(list_front_scan_ranges)
euclidian_coords = get_euclidian_coords(polar_coords)

# xpoints = []
# ypoints = []

# for sweep in euclidian_coords:
#     for p in sweep:
#         xpoints.append(p.x)
#         ypoints.append(p.y)
#         plt.scatter(xpoints, ypoints, s=1)
#         plt.pause(0.05)
#     plt.show()

# xpoints = [i for i in euclidian_coords[0].x]

output_file = open(output_file_path, "w")

for i in range(0, len(euclidian_coords)):
    output_file.write(f"sweep {i}\n")
    for p in euclidian_coords[i]:
        output_file.write(f"({p.x}, {p.y}), ")
    output_file.write("\n")
output_file.close()
input_file.close()






