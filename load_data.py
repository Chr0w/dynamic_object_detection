from data_types import EuclidianCoordinate
import jsonpickle
from munch import DefaultMunch
import statistics

def get_series(input_file_path):

    file = open(input_file_path, 'r')
    converted_data = file.read() # str
    file.close()

    data = jsonpickle.decode(converted_data)

    series = DefaultMunch.fromDict(data)

    add_center_of_mass(series)

    return series


def add_center_of_mass(series):
    for sweep in series.sweeps:
        if sweep.blobs:
            for blob in sweep.blobs:
                blob.center_of_mass = get_center_of_mass(blob)


def get_center_of_mass(blob):
    xpoints = []
    ypoints = []
    for p in blob.points:
        xpoints.append(p.x)
        ypoints.append(p.y)
    
    return EuclidianCoordinate(x=statistics.mean(xpoints), y=statistics.mean(ypoints))