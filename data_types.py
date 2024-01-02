from dataclasses import dataclass


@ dataclass
class raw_sweep:
    sec: int
    nsec: int
    ranges: list

@ dataclass
class PolarCoordinate:
    dist: float
    theta: float

@ dataclass
class EuclidianCoordinate:
    x: float
    y: float

@ dataclass
class ConvertedSweep:
    points: list[EuclidianCoordinate]

@ dataclass
class Series:
    sweeps: list[ConvertedSweep]