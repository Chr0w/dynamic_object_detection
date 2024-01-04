from dataclasses import dataclass
import json
# from pydantic import BaseModel

@ dataclass
class raw_sweep:
    sec: float
    ranges: list

@ dataclass
class EuclidianCoordinate:
    x: float
    y: float

@dataclass
class Blob:
    points: list[EuclidianCoordinate]
    center_of_mass: EuclidianCoordinate
    velocity_vector: tuple


@dataclass
class Sweep:
    sweep_nr: int
    all_points: list[EuclidianCoordinate]
    blobs: list[Blob]
    sec: float


@dataclass
class SweepSeries:
    sweeps: list[Sweep]

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)