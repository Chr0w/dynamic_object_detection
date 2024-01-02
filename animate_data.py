import sys
from data_types import *
from load_data import get_series


sweeps = get_series(sys.argv[1])

print(sweeps)