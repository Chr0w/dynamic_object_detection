from dataclasses import dataclass
import json
import numpy as np

@ dataclass
class raw_sweep:
    sec: float
    ranges: list

@ dataclass
class EuclidianCoordinate:
    x: float
    y: float
    label: int

@dataclass
class Blob:
    nr: int
    points: list[EuclidianCoordinate]
    center_of_mass: EuclidianCoordinate
    velocity_vector: tuple


@dataclass
class Sweep:
    sweep_nr: int
    all_points: list[EuclidianCoordinate]
    all_points_array: [[]]
    blobs: list[Blob]
    sec: float


@dataclass
class SweepSeries:
    sweeps: list[Sweep]

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)