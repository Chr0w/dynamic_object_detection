import sys
from dataclasses import dataclass
import math

import jsonpickle
# from pydantic import BaseModel
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

def get_series_from_scan(data):

    angle_min = 2.3998663425445557
    angle_increment = -0.0029088794253766537
    
    series = SweepSeries(sweeps=[])
    sweep_count = 0
    for s in data:
        sweep = Sweep(sweep_nr=sweep_count, points=[])
        sweep.sweep_nr = sweep_count
        for i in range(0, len(s.ranges)):
            angle = angle_min + (angle_increment * i)
            dist = float(s.ranges[i])
            if dist < 12:
                p = EuclidianCoordinate(x=math.cos(angle)*dist, y=math.sin(angle)*dist)
                sweep.points.append(p)

        series.sweeps.append(sweep)
        sweep_count += 1

    return series
    
# def get_euclidian_coords(polar_coords):
    
#     all_euclidian_coords = []

#     for sweep in polar_coords:
#         sweep_euclidian_coords = []

#         for p in sweep:
#             sweep_euclidian_coords.append(EuclidianCoordinate(x=math.cos(p.theta)*p.dist, y=math.sin(p.theta)*p.dist))
        
#         all_euclidian_coords.append(sweep_euclidian_coords)

#     return all_euclidian_coords


input_file_path = sys.argv[1]
output_file_path= sys.argv[2]
print(f"input_file: {input_file_path}")
print(f"output_file: {output_file_path}")


input_file = open(input_file_path, "r")


list_front_scan_ranges = get_front_scan_ranges(input_file)
series = get_series_from_scan(list_front_scan_ranges)

# print(json.dumps(series.toJson()))

output_file = open(output_file_path, "w")
# output_file.write(json.dumps(series.toJson(), indent=4))
output_file.write(jsonpickle.encode(series, unpicklable=False))

output_file.close()
input_file.close()
"""


for i in range(0, len(euclidian_coords)):
    output_file.write(f"sweep {i}\n")
    converted_sweep = ConvertedSweep
    for p in euclidian_coords[i]:
        converted_sweep.points.append(EuclidianCoordinate(x=p.x, y=p.y))    
    series.sweeps.append(EuclidianCoordinate(x=p.x, y=p.y))



output_file.write(json.dumps(point))
output_file.write("\n")
"""






