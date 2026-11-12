from __future__ import annotations

import math
from dataclasses import dataclass

from .vector3d import Vec3


@dataclass(slots=True)
class Vec4:
    """
    Four-dimensional vector.

    Commonly used for homogeneous coordinates in 3D graphics.
    """

    x: float
    y: float
    z: float
    w: float

    # --------------------------------------------------
    # Arithmetic
    # --------------------------------------------------

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
        return Vec4(-self.x, -self.y, -self.z, -self.w)

    # --------------------------------------------------
    # Length and normalization
    # --------------------------------------------------

    def length_squared(self) -> float:
        return (
            self.x**2
            + self.y**2
            + self.z**2
            + self.w**2
        )

    def length(self) -> float:
        return math.hypot(self.x, self.y, self.z, self.w)

    def normalized(self) -> Vec4:
        """
        Return a normalized copy.

        A zero vector remains a zero vector.
        """
        magnitude = self.length()

        if magnitude == 0:
            return Vec4(0.0, 0.0, 0.0, 0.0)

        return self / magnitude

    def normalize(self) -> None:
        """
        Normalize this vector in place.

        A zero vector remains unchanged.
        """
        magnitude = self.length()

        if magnitude == 0:
            return

        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude
        self.w /= magnitude

    # --------------------------------------------------
    # Vector operations
    # --------------------------------------------------

    def dot(self, other: Vec4) -> float:
        return (
            self.x * other.x
            + self.y * other.y
            + self.z * other.z
            + self.w * other.w
        )

    def distance_squared_to(self, other: Vec4) -> float:
        return (self - other).length_squared()

    def distance_to(self, other: Vec4) -> float:
        return math.sqrt(self.distance_squared_to(other))

    def is_zero(self, tolerance: float = 1e-9) -> bool:
        return self.length_squared() <= tolerance**2

    # --------------------------------------------------
    # Interpolation
    # --------------------------------------------------

    def lerp(self, other: Vec4, t: float) -> Vec4:
        """
        Linear interpolation between two vectors.

        t=0 returns self.
        t=1 returns other.
        """
        return self + (other - self) * t

    # --------------------------------------------------
    # Conversion
    # --------------------------------------------------

    @classmethod
    def from_vec3(cls, vector: Vec3, w: float = 1.0) -> Vec4:
        return cls(vector.x, vector.y, vector.z, w)

    def to_vec3(self) -> Vec3:
        """
        Convert homogeneous coordinates into Cartesian coordinates.
        """
        if self.w == 0:
            raise ValueError("Cannot convert a Vec4 with w=0 to a Vec3")

        return Vec3(
            self.x / self.w,
            self.y / self.w,
            self.z / self.w,
        )

    def xyz(self) -> Vec3:
        """Return the first three components without perspective division."""
        return Vec3(self.x, self.y, self.z)

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def copy(self) -> Vec4:
        return Vec4(self.x, self.y, self.z, self.w)
