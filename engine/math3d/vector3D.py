from __future__ import annotations
from dataclasses import dataclass

import math


@dataclass(slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vec3:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vec3:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vec3:
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def length(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def length_squared(self) -> float:
        return self.x**2 + self.y**2 + self.z**2

    def normalized(self) -> Vec3:
        length_squared = self.length_squared()
        if length_squared == 0:
            return Vec3(0.0, 0.0, 0.0)
        return self / math.sqrt(length_squared)

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def distance_to(self, other: Vec3) -> float:
        return math.hypot(self.x - other.x, self.y - other.y, self.z - other.z)
