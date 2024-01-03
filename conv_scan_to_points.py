import sys
import math
import jsonpickle
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
    
    ANGLE_OFFSET = math.pi/4
    X_OFFSET = 1.2
    Y_OFFSET = 1

    series = SweepSeries(sweeps=[])
    sweep_count = 0
    for s in data:
        sweep = Sweep(sweep_nr=sweep_count, points=[])
        sweep.sweep_nr = sweep_count
        for i in range(0, len(s.ranges)):
            angle = angle_min + (angle_increment * i) + ANGLE_OFFSET
            dist = float(s.ranges[i])
            if dist < 8 and dist > 0.1:
                p = EuclidianCoordinate(x=math.cos(angle)*dist+X_OFFSET, y=math.sin(angle)*dist+Y_OFFSET)
                sweep.points.append(p)

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




