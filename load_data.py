import sys
from dataclasses import dataclass
import math
import json
from json import JSONEncoder
from data_types import *
import jsonpickle
from munch import DefaultMunch



def get_series(input_file_path):

    file = open(input_file_path, 'r')
    converted_data = file.read() # str
    file.close()

    data = jsonpickle.decode(converted_data)

    obj = DefaultMunch.fromDict(data)

    # series = SweepSeries(**data)

    return obj



    # for line in converted_data:
    #     if not "sweep" in line:
    #         sweep = ConvertedSweep
    #         all_points = line.split("),(")
    #         # series.sweeps.append()
    #         for p in all_points:
    #             # sweep.points.append(EuclidianCoordinate(x=))
    #             # ConvertedSweep
    #             print(p)
    #         break

