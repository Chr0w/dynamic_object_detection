from data_types import EuclidianCoordinate, SweepSeries, Blob
import jsonpickle
from munch import DefaultMunch
import numpy as np
import statistics
import copy
import math
from scipy.cluster.hierarchy import fclusterdata


def get_series(input_file_path):

    file = open(input_file_path, 'r')
    converted_data = file.read() # str
    file.close()

    data = jsonpickle.decode(converted_data)

    series: SweepSeries = DefaultMunch.fromDict(data)

    for sweep in series.sweeps:
        y_pred = fclusterdata(sweep.all_points_array, 0.3, criterion='distance')
        
        for i in range(0, len(sweep.all_points)):
            sweep.all_points[i].label = y_pred[i]

    add_center_of_mass(series)

    return series


def add_center_of_mass(series):
    for sweep in series.sweeps:
        if sweep.blobs:
            for blob in sweep.blobs:
                blob.center_of_mass = get_center_of_mass(blob)



# def within_threshold(p, list):
#     THRESHOLD = 0.2  # meter
#     for target in list:
#         if get_dist(target, p) < THRESHOLD:
#             return True
#     return False

# def get_dist(a, b):
#     return math.sqrt((a.y - b.y)**2 + (a.x - b.x)**2)


def get_center_of_mass(points):
    xpoints = []
    ypoints = []
    for p in points:
        xpoints.append(p.x)
        ypoints.append(p.y)
    
    return EuclidianCoordinate(x=statistics.mean(xpoints), y=statistics.mean(ypoints))