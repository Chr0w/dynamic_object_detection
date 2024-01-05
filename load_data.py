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
        point_lables = fclusterdata(sweep.all_points_array, 0.3, criterion='distance')

        for i in range(0, len(sweep.all_points)):
            sweep.all_points[i].label = point_lables[i]-1

        sweep.blobs = get_blobs(sweep, point_lables)

        # print(f"Number of blobs in sweep: {len(sweep.blobs)}")

        for b in sweep.blobs: 
            b.center_of_mass = get_center_of_mass(b.points)
            # print(f"blob {b.nr} CoM: {b.center_of_mass}")

    add_velocity_vector(series)

    #smooth_vectors_running_average(series)

    return series

"""
def smooth_vectors_running_average(series):

    for i in range(0, len(series.sweeps)):
        if i < 2:
            continue
        no_blobs = len(series.sweeps[i].blobs)

        for j in range(0, no_blobs-1):
            avg_x = (series.sweeps[i-2].blobs[j].velocity_vector[0] + series.sweeps[i-1].blobs[j].velocity_vector[0] + series.sweeps[i].blobs[j].velocity_vector[0]) / 3
            avg_y = (series.sweeps[i-2].blobs[j].velocity_vector[1] + series.sweeps[i-1].blobs[j].velocity_vector[1] + series.sweeps[i].blobs[j].velocity_vector[1]) / 3

            smooth_vector = (avg_x, avg_y)
            series.sweeps[i].blobs[j].velocity_vector_smooth = smooth_vector
"""

def get_blobs(sweep, point_lables):

    blob_list: list[Blob] = []
    for i in range(0, max(point_lables)):
        b = Blob(nr=i, points=[], center_of_mass=None, velocity_vector=[0,0], velocity_vector_smooth=None)
        blob_list.append(b)

    for p in sweep.all_points:
        blob_list[(p.label)].points.append(p)

    return blob_list


def add_center_of_mass(series):
    for sweep in series.sweeps:
        if sweep.blobs:
            for blob in sweep.blobs:
                blob.center_of_mass = get_center_of_mass(blob)


def add_velocity_vector(series):
    for index, sweep in enumerate(series.sweeps):
        if index == 0:
            #print("******SKIP FIRST <SWEEP!!!!")
            continue
        #print("got to calculate_velocity")
        velocity_vector_list = calculate_velocity_for_current_sweep(series.sweeps[index-1], sweep)
    
        #print(f"no blobs: {len(sweep.blobs)}")
        #print(f"no vectors: {len(velocity_vector_list)}")
        #exit()

        for i, v in enumerate(velocity_vector_list):
            sweep.blobs[i].velocity_vector = v
    #return series

def calculate_velocity_for_current_sweep(previous_sweep, current_sweep):

    velocity_vector_list = []
    previous_sweep_copy = copy.deepcopy(previous_sweep)
    for cur_blob in current_sweep.blobs:
        for prev_blob in previous_sweep_copy.blobs:
            delta_x_squared = math.pow(cur_blob.center_of_mass.x - prev_blob.center_of_mass.x, 2)
            delta_y_squared = math.pow(cur_blob.center_of_mass.y - prev_blob.center_of_mass.y, 2)
            radius = math.sqrt(delta_x_squared + delta_y_squared)
            if radius < 0.5:
                delta_time = current_sweep.sec - previous_sweep_copy.sec
                vector = GetVelocityVector(prev_blob, cur_blob, delta_time)
                velocity_vector_list.append(vector)
                #cur_blob.velocity_vector = vector
                #print(cur_blob.velocity_vector)
                previous_sweep_copy.blobs.remove(prev_blob)
                break
    return velocity_vector_list

def GetVelocityVector(prev_blob, cur_blob, delta_time):
    velocity_x = (cur_blob.center_of_mass.x - prev_blob.center_of_mass.x) / delta_time
    velocity_y = (cur_blob.center_of_mass.y - prev_blob.center_of_mass.y) / delta_time
    return velocity_x, velocity_y

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
    
    return EuclidianCoordinate(x=statistics.mean(xpoints), y=statistics.mean(ypoints), label=p.label)