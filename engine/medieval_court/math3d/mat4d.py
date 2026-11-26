from __future__ import annotations

import math
from dataclasses import dataclass
from typing import overload

from .mat3d import Mat3
from .vector3d import Vec3
from .vector4d import Vec4


@dataclass(slots=True)
class Mat4:
    """
    Represent a 4x4 transformation matrix.

    Convention:
    - Row-major storage.
    - Column vectors.
    - M @ v.
    - Transformations are applied right-to-left.

    Example:
        projection @ view @ model @ position
    """

    m00: float
    m01: float
    m02: float
    m03: float

    m10: float
    m11: float
    m12: float
    m13: float

    m20: float
    m21: float
    m22: float
    m23: float

    m30: float
    m31: float
    m32: float
    m33: float

    # ==================================================
    # CONSTRUCTION
    # ==================================================

    @classmethod
    def identity(cls) -> Mat4:
        """Return the identity matrix."""

        return cls(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def translation(cls, position: Vec3) -> Mat4:
        """Return a translation matrix."""

        return cls(
            1.0, 0.0, 0.0, position.x,
            0.0, 1.0, 0.0, position.y,
            0.0, 0.0, 1.0, position.z,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def scale(cls, scale: Vec3) -> Mat4:
        """Return a scaling matrix."""

        return cls(
            scale.x, 0.0, 0.0, 0.0,
            0.0, scale.y, 0.0, 0.0,
            0.0, 0.0, scale.z, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_x(cls, angle: float) -> Mat4:
        """Return a rotation matrix around the X axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            1.0, 0.0, 0.0, 0.0,
            0.0, c, -s, 0.0,
            0.0, s, c, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_y(cls, angle: float) -> Mat4:
        """Return a rotation matrix around the Y axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, 0.0, s, 0.0,
            0.0, 1.0, 0.0, 0.0,
            -s, 0.0, c, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_z(cls, angle: float) -> Mat4:
        """Return a rotation matrix around the Z axis."""

        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, -s, 0.0, 0.0,
            s, c, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def perspective(
        cls,
        fov: float,
        aspect: float,
        near: float,
        far: float,
    ) -> Mat4:
        """Return a perspective projection matrix."""

        if not 0.0 < fov < math.pi:
            raise ValueError("fov must be between 0 and pi radians")

        if aspect <= 0.0:
            raise ValueError("aspect must be greater than zero")

        if not 0.0 < near < far:
            raise ValueError("Expected 0 < near < far")

        f = 1.0 / math.tan(fov * 0.5)

        return cls(
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0, (far + near) / (near - far),
            (2.0 * far * near) / (near - far),
            0.0, 0.0, -1.0, 0.0,
        )

    @classmethod
    def orthographic(
        cls,
        left: float,
        right: float,
        bottom: float,
        top: float,
        near: float,
        far: float,
    ) -> Mat4:
        """Return an orthographic projection matrix."""

        if right == left:
            raise ValueError("left and right cannot be equal")

        if top == bottom:
            raise ValueError("bottom and top cannot be equal")

        if far == near:
            raise ValueError("near and far cannot be equal")

        return cls(
            2.0 / (right - left), 0.0, 0.0,
            -(right + left) / (right - left),

            0.0, 2.0 / (top - bottom), 0.0,
            -(top + bottom) / (top - bottom),

            0.0, 0.0, -2.0 / (far - near),
            -(far + near) / (far - near),

            0.0, 0.0, 0.0, 1.0,
        )

    # ==================================================
    # MULTIPLICATION
    # ==================================================

    @overload
    def __matmul__(self, other: Mat4) -> Mat4: ...

    @overload
    def __matmul__(self, other: Vec4) -> Vec4: ...

    def __matmul__(self, other: Mat4 | Vec4) -> Mat4 | Vec4:
        """Multiply this matrix by another matrix or vector."""

        if isinstance(other, Vec4):
            return self._multiply_vector(other)

        if isinstance(other, Mat4):
            return self._multiply_matrix(other)

        return NotImplemented

    def _multiply_vector(self, vector: Vec4) -> Vec4:
        """Multiply this matrix by a homogeneous vector."""

        x, y, z, w = vector.x, vector.y, vector.z, vector.w

        return Vec4(
            self.m00 * x + self.m01 * y + self.m02 * z + self.m03 * w,
            self.m10 * x + self.m11 * y + self.m12 * z + self.m13 * w,
            self.m20 * x + self.m21 * y + self.m22 * z + self.m23 * w,
            self.m30 * x + self.m31 * y + self.m32 * z + self.m33 * w,
        )

    def _multiply_matrix(self, other: Mat4) -> Mat4:
        """Multiply this matrix by another 4x4 matrix."""

        a = self
        b = other

        return Mat4(
            a.m00*b.m00 + a.m01*b.m10 + a.m02*b.m20 + a.m03*b.m30,
            a.m00*b.m01 + a.m01*b.m11 + a.m02*b.m21 + a.m03*b.m31,
            a.m00*b.m02 + a.m01*b.m12 + a.m02*b.m22 + a.m03*b.m32,
            a.m00*b.m03 + a.m01*b.m13 + a.m02*b.m23 + a.m03*b.m33,

            a.m10*b.m00 + a.m11*b.m10 + a.m12*b.m20 + a.m13*b.m30,
            a.m10*b.m01 + a.m11*b.m11 + a.m12*b.m21 + a.m13*b.m31,
            a.m10*b.m02 + a.m11*b.m12 + a.m12*b.m22 + a.m13*b.m32,
            a.m10*b.m03 + a.m11*b.m13 + a.m12*b.m23 + a.m13*b.m33,

            a.m20*b.m00 + a.m21*b.m10 + a.m22*b.m20 + a.m23*b.m30,
            a.m20*b.m01 + a.m21*b.m11 + a.m22*b.m21 + a.m23*b.m31,
            a.m20*b.m02 + a.m21*b.m12 + a.m22*b.m22 + a.m23*b.m32,
            a.m20*b.m03 + a.m21*b.m13 + a.m22*b.m23 + a.m23*b.m33,

            a.m30*b.m00 + a.m31*b.m10 + a.m32*b.m20 + a.m33*b.m30,
            a.m30*b.m01 + a.m31*b.m11 + a.m32*b.m21 + a.m33*b.m31,
            a.m30*b.m02 + a.m31*b.m12 + a.m32*b.m22 + a.m33*b.m32,
            a.m30*b.m03 + a.m31*b.m13 + a.m32*b.m23 + a.m33*b.m33,
        )

    # ==================================================
    # MATRIX OPERATIONS
    # ==================================================

    def transpose(self) -> Mat4:
        """Return the transposed matrix."""

        return Mat4(
            self.m00, self.m10, self.m20, self.m30,
            self.m01, self.m11, self.m21, self.m31,
            self.m02, self.m12, self.m22, self.m32,
            self.m03, self.m13, self.m23, self.m33,
        )

    def inverse(self) -> Mat4:
        """Return the inverse using Gauss-Jordan elimination."""

        rows = [
            [self.m00, self.m01, self.m02, self.m03, 1.0, 0.0, 0.0, 0.0],
            [self.m10, self.m11, self.m12, self.m13, 0.0, 1.0, 0.0, 0.0],
            [self.m20, self.m21, self.m22, self.m23, 0.0, 0.0, 1.0, 0.0],
            [self.m30, self.m31, self.m32, self.m33, 0.0, 0.0, 0.0, 1.0],
        ]

        for column in range(4):
            self._pivot(rows, column)
            self._normalize_pivot(rows, column)
            self._eliminate_column(rows, column)

        return Mat4(
            *(
                value
                for row in rows
                for value in row[4:]
            )
        )

    @staticmethod
    def _pivot(rows: list[list[float]], column: int) -> None:
        """Select the pivot using partial pivoting."""

        pivot = max(
            range(column, 4),
            key=lambda row: abs(rows[row][column]),
        )

        if math.isclose(
            rows[pivot][column],
            0.0,
            abs_tol=1e-12,
        ):
            raise ValueError("Matrix is not invertible.")

        rows[column], rows[pivot] = rows[pivot], rows[column]

    @staticmethod
    def _normalize_pivot(rows: list[list[float]], column: int) -> None:
        """Normalize the pivot row."""

        pivot = rows[column][column]

        for j in range(8):
            rows[column][j] /= pivot

    @staticmethod
    def _eliminate_column(rows: list[list[float]], column: int) -> None:
        """Eliminate the other entries in the pivot column."""

        for row in range(4):
            if row == column:
                continue

            factor = rows[row][column]

            if factor == 0.0:
                continue

            for j in range(8):
                rows[row][j] -= factor * rows[column][j]

    # ==================================================
    # TRANSFORMATIONS
    # ==================================================

    def transform_point(self, point: Vec3) -> Vec3:
        """Transform a position using homogeneous coordinates."""

        result = self @ Vec4(
            point.x,
            point.y,
            point.z,
            1.0,
        )

        if not isinstance(result, Vec4):
            raise TypeError("Unexpected matrix multiplication result.")

        if math.isclose(result.w, 0.0, abs_tol=1e-12):
            raise ValueError("Transformed point has zero homogeneous coordinate.")

        return Vec3(
            result.x / result.w,
            result.y / result.w,
            result.z / result.w,
        )

    def transform_direction(self, direction: Vec3) -> Vec3:
        """Transform a direction without applying translation."""

        result = self @ Vec4(
            direction.x,
            direction.y,
            direction.z,
            0.0,
        )

        if not isinstance(result, Vec4):
            raise TypeError("Unexpected matrix multiplication result.")

        return Vec3(
            result.x,
            result.y,
            result.z,
        )

    def normal_matrix(self) -> Mat3:
        """Return the inverse-transpose of the upper-left 3x3 matrix."""

        linear = Mat3(
            self.m00, self.m01, self.m02,
            self.m10, self.m11, self.m12,
            self.m20, self.m21, self.m22,
        )

        return linear.inverse().transpose()
