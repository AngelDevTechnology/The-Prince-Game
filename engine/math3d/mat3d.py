from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from .vector3d import Vec3

if TYPE_CHECKING:
    from .mat4d import Mat4


@dataclass(slots=True)
class Mat3:
    """
    Represent a 3x3 matrix.

    Convention:
    - Row-major storage.
    - Column vectors.
    - M @ v.
    - Transformations are applied right-to-left.

    Used for:
    - Rotations.
    - Directions.
    - Normals.
    - Bases.
    - Extracting the linear part of a Mat4.
    """

    m00: float
    m01: float
    m02: float

    m10: float
    m11: float
    m12: float

    m20: float
    m21: float
    m22: float

    # ==================================================
    # CONSTRUCTION
    # ==================================================

    @classmethod
    def identity(cls) -> Mat3:
        """Return the identity matrix."""

        return cls(
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_x(cls, angle: float) -> Mat3:
        """Return a rotation matrix around the X axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            1.0, 0.0, 0.0,
            0.0, c, -s,
            0.0, s, c,
        )

    @classmethod
    def rotation_y(cls, angle: float) -> Mat3:
        """Return a rotation matrix around the Y axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, 0.0, s,
            0.0, 1.0, 0.0,
            -s, 0.0, c,
        )

    @classmethod
    def rotation_z(cls, angle: float) -> Mat3:
        """Return a rotation matrix around the Z axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, -s, 0.0,
            s, c, 0.0,
            0.0, 0.0, 1.0,
        )

    @classmethod
    def from_mat4(cls, matrix: Mat4) -> Mat3:
        """Extract the upper-left 3x3 linear part of a Mat4."""

        return cls(
            matrix.m00, matrix.m01, matrix.m02,
            matrix.m10, matrix.m11, matrix.m12,
            matrix.m20, matrix.m21, matrix.m22,
        )

    # ==================================================
    # MULTIPLICATION
    # ==================================================

    @overload
    def __matmul__(self, other: Mat3) -> Mat3: ...

    @overload
    def __matmul__(self, other: Vec3) -> Vec3: ...

    def __matmul__(self, other: Mat3 | Vec3) -> Mat3 | Vec3:
        """Multiply this matrix by another matrix or vector."""

        if isinstance(other, Vec3):
            return self._multiply_vector(other)

        if isinstance(other, Mat3):
            return self._multiply_matrix(other)

        return NotImplemented

    def _multiply_vector(self, vector: Vec3) -> Vec3:
        """Multiply this matrix by a vector."""

        x, y, z = vector.x, vector.y, vector.z

        return Vec3(
            self.m00 * x + self.m01 * y + self.m02 * z,
            self.m10 * x + self.m11 * y + self.m12 * z,
            self.m20 * x + self.m21 * y + self.m22 * z,
        )

    def _multiply_matrix(self, other: Mat3) -> Mat3:
        """Multiply this matrix by another 3x3 matrix."""

        a = self
        b = other

        return Mat3(
            a.m00 * b.m00 + a.m01 * b.m10 + a.m02 * b.m20,
            a.m00 * b.m01 + a.m01 * b.m11 + a.m02 * b.m21,
            a.m00 * b.m02 + a.m01 * b.m12 + a.m02 * b.m22,

            a.m10 * b.m00 + a.m11 * b.m10 + a.m12 * b.m20,
            a.m10 * b.m01 + a.m11 * b.m11 + a.m12 * b.m21,
            a.m10 * b.m02 + a.m11 * b.m12 + a.m12 * b.m22,

            a.m20 * b.m00 + a.m21 * b.m10 + a.m22 * b.m20,
            a.m20 * b.m01 + a.m21 * b.m11 + a.m22 * b.m21,
            a.m20 * b.m02 + a.m21 * b.m12 + a.m22 * b.m22,
        )

    # ==================================================
    # MATRIX OPERATIONS
    # ==================================================

    def transpose(self) -> Mat3:
        """Return the transposed matrix."""

        return Mat3(
            self.m00, self.m10, self.m20,
            self.m01, self.m11, self.m21,
            self.m02, self.m12, self.m22,
        )

    def determinant(self) -> float:
        """Calculate the determinant of this matrix."""

        return (
            self.m00 * (self.m11 * self.m22 - self.m12 * self.m21)
            - self.m01 * (self.m10 * self.m22 - self.m12 * self.m20)
            + self.m02 * (self.m10 * self.m21 - self.m11 * self.m20)
        )

    def inverse(self) -> Mat3:
        """Return the inverse of this matrix."""

        determinant = self.determinant()

        if math.isclose(determinant, 0.0, abs_tol=1e-12):
            raise ValueError("Matrix is not invertible.")

        inv_det = 1.0 / determinant

        return Mat3(
            (self.m11 * self.m22 - self.m12 * self.m21) * inv_det,
            (self.m02 * self.m21 - self.m01 * self.m22) * inv_det,
            (self.m01 * self.m12 - self.m02 * self.m11) * inv_det,

            (self.m12 * self.m20 - self.m10 * self.m22) * inv_det,
            (self.m00 * self.m22 - self.m02 * self.m20) * inv_det,
            (self.m02 * self.m10 - self.m00 * self.m12) * inv_det,

            (self.m10 * self.m21 - self.m11 * self.m20) * inv_det,
            (self.m01 * self.m20 - self.m00 * self.m21) * inv_det,
            (self.m00 * self.m11 - self.m01 * self.m10) * inv_det,
        )

    # ==================================================
    # TRANSFORMATIONS
    # ==================================================

    def transform_direction(self, direction: Vec3) -> Vec3:
        """Transform a direction vector."""

        return self._multiply_vector(direction)

    def normal_matrix(self) -> Mat3:
        """Return the inverse-transpose matrix used for normal transformations."""

        return self.inverse().transpose()
