from dataclasses import dataclass
from data_types import *
import jsonpickle
from munch import DefaultMunch

def get_series(input_file_path):

    file = open(input_file_path, 'r')
    converted_data = file.read() # str
    file.close()

    data = jsonpickle.decode(converted_data)

    obj = DefaultMunch.fromDict(data)

    return obj
