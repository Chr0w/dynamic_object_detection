import sys
import math
import jsonpickle
import re
from data_types import *
import numpy as np

def get_front_scan_ranges(input_file):

    start_seconds_offset = None

    all_ranges = []
    front_scanner = False
    for line in input_file:
        if "front_laser_link" in line:
            front_scanner = True
            continue

        elif "back_laser_link" in line:
            front_scanner = False  
            continue

        elif "nsecs" in line:
            time_stamp_nanoseconds = float(re.findall(r'\d+',line)[0])*pow(10,-9)
            continue

        if "secs" in line:
            time_stamp_seconds = float(re.findall(r'\d+',line)[0])
            if not start_seconds_offset:
                start_seconds_offset = time_stamp_seconds
            continue

        if front_scanner and "ranges" in line:
            ranges_as_string = line[9:len(line)-2]
            ranges_as_list = list(ranges_as_string.split(", "))

            all_ranges.append(raw_sweep(ranges=ranges_as_list, sec= (time_stamp_seconds-start_seconds_offset)+time_stamp_nanoseconds))

    return all_ranges

def get_series_from_scan(data):

    angle_min = 2.3998663425445557
    angle_increment = -0.0029088794253766537
    
    ANGLE_OFFSET = math.pi/4
    X_OFFSET = 1.2
    Y_OFFSET = 1

    series = SweepSeries(sweeps=[])
    sweep_count = 0
    for s in data:
        sweep = Sweep(sweep_nr=sweep_count, all_points=[], blobs = [], sec = 0, all_points_array=[])
        sweep.sweep_nr = sweep_count
        for i in range(0, len(s.ranges)):
            angle = angle_min + (angle_increment * i) + ANGLE_OFFSET
            dist = float(s.ranges[i])
            if dist < 8 and dist > 0.1:
                p = EuclidianCoordinate(x=math.cos(angle)*dist+X_OFFSET, y=math.sin(angle)*dist+Y_OFFSET, label=0)
                sweep.all_points.append(p)
                xy_array = [p.x, p.y]
                sweep.all_points_array.append(xy_array)


        sweep.sec = s.sec
        series.sweeps.append(sweep)
        sweep_count += 1

    return series

input_file_path = sys.argv[1]
output_file_path= sys.argv[2]
print(f"input_file: {input_file_path}")
print(f"output_file: {output_file_path}")

input_file = open(input_file_path, "r")

list_front_scan_ranges = get_front_scan_ranges(input_file)
series = get_series_from_scan(list_front_scan_ranges)

output_file = open(output_file_path, "w")
output_file.write(jsonpickle.encode(series, unpicklable=False))

output_file.close()
input_file.close()




