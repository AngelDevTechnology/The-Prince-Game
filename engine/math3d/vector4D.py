from __future__ import annotations

from dataclasses import dataclass
import math

from .vector3D import Vec3


@dataclass(slots=True)
class Vec4:
    x: float
    y: float
    z: float
    w: float

    def __add__(self, other: Vec4) -> Vec4:
        return Vec4(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w,
        )

    def __sub__(self, other: Vec4) -> Vec4:
        return Vec4(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w,
        )

    def __mul__(self, scalar: float) -> Vec4:
        return Vec4(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
            self.w * scalar,
        )

    def __rmul__(self, scalar: float) -> Vec4:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vec4:
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide Vec4 by zero")

        return Vec4(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
            self.w / scalar,
        )

    def __neg__(self) -> Vec4:
        return Vec4(
            -self.x,
            -self.y,
            -self.z,
            -self.w,
        )

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        return (
            self.x**2 +
            self.y**2 +
            self.z**2 +
            self.w**2
        )

    def normalized(self) -> Vec4:
        length_squared = self.length_squared()

        if length_squared == 0:
            return Vec4(0.0, 0.0, 0.0, 0.0)

        return self / math.sqrt(length_squared)

    def dot(self, other: Vec4) -> float:
        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z +
            self.w * other.w
        )

    @classmethod
    def from_vec3(cls, vector: Vec3, w: float = 1.0) -> Vec4:
        return cls(
            vector.x,
            vector.y,
            vector.z,
            w,
        )

    def to_vec3(self) -> Vec3:
        if self.w == 0:
            raise ValueError(
                "Cannot convert a Vec4 with w=0 to a Vec3"
            )

        return Vec3(
            self.x / self.w,
            self.y / self.w,
            self.z / self.w,
        )