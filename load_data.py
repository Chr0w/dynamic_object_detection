import sys
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
from data_types import *





def get_series(input_file_path):

    converted_data = open(input_file_path, 'r')

    for line in converted_data:
        if not "sweep" in line:
            all_points = line.split(", ")

            for p in all_points:
                print(p)
            break

