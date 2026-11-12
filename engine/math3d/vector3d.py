from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(slots=True)
class Vec3:
    """
    Represent a three-dimensional vector.

    Supports:
    - Arithmetic operations.
    - Vector products.
    - Geometric measurements.
    - Normalization.
    - Interpolation.
    - Direction transformations.
    """

    x: float
    y: float
    z: float

    # ==================================================
    # ARITHMETIC
    # ==================================================

    def __add__(self, other: Vec3) -> Vec3:
        """Add two vectors."""

        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Vec3) -> Vec3:
        """Subtract two vectors."""

        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, scalar: float) -> Vec3:
        """Multiply the vector by a scalar."""

        return Vec3(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __rmul__(self, scalar: float) -> Vec3:
        """Support scalar multiplication from the left."""

        return self * scalar

    def __truediv__(self, scalar: float) -> Vec3:
        """Divide the vector by a scalar."""

        if scalar == 0.0:
            raise ZeroDivisionError("Cannot divide by zero.")

        return Vec3(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
        )

    def __neg__(self) -> Vec3:
        """Return the opposite vector."""

        return Vec3(
            -self.x,
            -self.y,
            -self.z,
        )

    # ==================================================
    # VECTOR PRODUCTS
    # ==================================================

    def dot(self, other: Vec3) -> float:
        """Calculate the dot product."""

        return (
            self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )

    def cross(self, other: Vec3) -> Vec3:
        """Calculate the cross product."""

        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def hadamard(self, other: Vec3) -> Vec3:
        """Multiply two vectors component-wise."""

        return Vec3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )

    # ==================================================
    # LENGTH AND DISTANCE
    # ==================================================

    def length(self) -> float:
        """Calculate the vector magnitude."""

        return math.hypot(
            self.x,
            self.y,
            self.z,
        )

    def length_squared(self) -> float:
        """Calculate the squared vector magnitude."""

        return self.dot(self)

    def distance_to(self, other: Vec3) -> float:
        """Calculate the distance to another vector."""

        return (self - other).length()

    def distance_squared_to(self, other: Vec3) -> float:
        """Calculate the squared distance to another vector."""

        return (self - other).length_squared()

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def normalized(self) -> Vec3:
        """Return a normalized copy of this vector."""

        length = self.length()

        if length == 0.0:
            return Vec3(0.0, 0.0, 0.0)

        return self / length

    def normalize(self) -> None:
        """Normalize this vector in place."""

        length = self.length()

        if length == 0.0:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            return

        self.x /= length
        self.y /= length
        self.z /= length

    def is_zero(self) -> bool:
        """Check whether the vector is exactly zero."""

        return (
            self.x == 0.0
            and self.y == 0.0
            and self.z == 0.0
        )

    # ==================================================
    # GEOMETRY
    # ==================================================

    def angle_to(self, other: Vec3) -> float:
        """Calculate the angle between two vectors in radians."""

        denominator = self.length() * other.length()

        if denominator == 0.0:
            raise ValueError("Cannot calculate an angle with a zero vector.")

        cosine = self.dot(other) / denominator
        cosine = max(-1.0, min(1.0, cosine))

        return math.acos(cosine)

    def reflected(self, normal: Vec3) -> Vec3:
        """Reflect this vector around a normalized surface normal."""

        return self - normal * (2.0 * self.dot(normal))

    def project_onto(self, other: Vec3) -> Vec3:
        """Project this vector onto another vector."""

        denominator = other.length_squared()

        if denominator == 0.0:
            raise ValueError("Cannot project onto a zero vector.")

        return other * (self.dot(other) / denominator)

    # ==================================================
    # INTERPOLATION
    # ==================================================

    def lerp(self, other: Vec3, t: float) -> Vec3:
        """Linearly interpolate between two vectors."""

        return self + (other - self) * t

    # ==================================================
    # UTILITY
    # ==================================================

    def copy(self) -> Vec3:
        """Return an independent copy of this vector."""

        return Vec3(
            self.x,
            self.y,
            self.z,
        )

    def __repr__(self) -> str:
        return f"Vec3(x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"
