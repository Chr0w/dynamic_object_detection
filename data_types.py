from dataclasses import dataclass
import json
# from pydantic import BaseModel

@ dataclass
class raw_sweep:
    sec: int
    nsec: int
    ranges: list

@ dataclass
class EuclidianCoordinate:
    x: float
    y: float

@ dataclass
class Sweep:
    sweep_nr: int
    points: list[EuclidianCoordinate]

@ dataclass
class SweepSeries:
    sweeps: list[Sweep]

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)