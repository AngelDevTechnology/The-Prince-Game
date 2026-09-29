from __future__ import annotations

from dataclasses import dataclass
import math

from .vector3D import Vec3
from .vector4D import Vec4


@dataclass(slots=True)
class Mat4:
    """
    4x4 matrix.

    Convention:
    - row-major storage
    - column vectors
    - M @ v
    - transformations are applied right-to-left

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

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def identity(cls) -> Mat4:
        return cls(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def translation(cls, position: Vec3) -> Mat4:
        return cls(
            1.0, 0.0, 0.0, position.x,
            0.0, 1.0, 0.0, position.y,
            0.0, 0.0, 1.0, position.z,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def scale(cls, scale: Vec3) -> Mat4:
        return cls(
            scale.x, 0.0, 0.0, 0.0,
            0.0, scale.y, 0.0, 0.0,
            0.0, 0.0, scale.z, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_x(cls, angle: float) -> Mat4:
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
        if aspect <= 0.0:
            raise ValueError("aspect must be greater than zero")

        if not 0.0 < near < far:
            raise ValueError("Expected 0 < near < far")

        if not 0.0 < fov < math.pi:
            raise ValueError("fov must be between 0 and pi radians")

        f = 1.0 / math.tan(fov * 0.5)

        return cls(
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0,
            (far + near) / (near - far),
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
        if right == left:
            raise ValueError("left and right cannot be equal")

        if top == bottom:
            raise ValueError("bottom and top cannot be equal")

        if far == near:
            raise ValueError("near and far cannot be equal")

        return cls(
            2.0 / (right - left),
            0.0,
            0.0,
            -(right + left) / (right - left),

            0.0,
            2.0 / (top - bottom),
            0.0,
            -(top + bottom) / (top - bottom),

            0.0,
            0.0,
            -2.0 / (far - near),
            -(far + near) / (far - near),

            0.0,
            0.0,
            0.0,
            1.0,
        )

    # ------------------------------------------------------------------
    # Multiplication
    # ------------------------------------------------------------------

    def __matmul__(self, other: Mat4 | Vec4) -> Mat4 | Vec4:
        # --------------------------------------------------------------
        # Mat4 @ Vec4
        # --------------------------------------------------------------

        if isinstance(other, Vec4):
            x = other.x
            y = other.y
            z = other.z
            w = other.w

            return Vec4(
                self.m00 * x
                + self.m01 * y
                + self.m02 * z
                + self.m03 * w,

                self.m10 * x
                + self.m11 * y
                + self.m12 * z
                + self.m13 * w,

                self.m20 * x
                + self.m21 * y
                + self.m22 * z
                + self.m23 * w,

                self.m30 * x
                + self.m31 * y
                + self.m32 * z
                + self.m33 * w,
            )

        # --------------------------------------------------------------
        # Mat4 @ Mat4
        # --------------------------------------------------------------

        if isinstance(other, Mat4):
            a00, a01, a02, a03 = (
                self.m00,
                self.m01,
                self.m02,
                self.m03,
            )
            a10, a11, a12, a13 = (
                self.m10,
                self.m11,
                self.m12,
                self.m13,
            )
            a20, a21, a22, a23 = (
                self.m20,
                self.m21,
                self.m22,
                self.m23,
            )
            a30, a31, a32, a33 = (
                self.m30,
                self.m31,
                self.m32,
                self.m33,
            )

            b00, b01, b02, b03 = (
                other.m00,
                other.m01,
                other.m02,
                other.m03,
            )
            b10, b11, b12, b13 = (
                other.m10,
                other.m11,
                other.m12,
                other.m13,
            )
            b20, b21, b22, b23 = (
                other.m20,
                other.m21,
                other.m22,
                other.m23,
            )
            b30, b31, b32, b33 = (
                other.m30,
                other.m31,
                other.m32,
                other.m33,
            )

            return Mat4(
                a00 * b00 + a01 * b10 + a02 * b20 + a03 * b30,
                a00 * b01 + a01 * b11 + a02 * b21 + a03 * b31,
                a00 * b02 + a01 * b12 + a02 * b22 + a03 * b32,
                a00 * b03 + a01 * b13 + a02 * b23 + a03 * b33,

                a10 * b00 + a11 * b10 + a12 * b20 + a13 * b30,
                a10 * b01 + a11 * b11 + a12 * b21 + a13 * b31,
                a10 * b02 + a11 * b12 + a12 * b22 + a13 * b32,
                a10 * b03 + a11 * b13 + a12 * b23 + a13 * b33,

                a20 * b00 + a21 * b10 + a22 * b20 + a23 * b30,
                a20 * b01 + a21 * b11 + a22 * b21 + a23 * b31,
                a20 * b02 + a21 * b12 + a22 * b22 + a23 * b32,
                a20 * b03 + a21 * b13 + a22 * b23 + a23 * b33,

                a30 * b00 + a31 * b10 + a32 * b20 + a33 * b30,
                a30 * b01 + a31 * b11 + a32 * b21 + a33 * b31,
                a30 * b02 + a31 * b12 + a32 * b22 + a33 * b32,
                a30 * b03 + a31 * b13 + a32 * b23 + a33 * b33,
            )

        return NotImplemented

    # ------------------------------------------------------------------
    # Matrix operations
    # ------------------------------------------------------------------

    def transpose(self) -> Mat4:
        return Mat4(
            self.m00,
            self.m10,
            self.m20,
            self.m30,

            self.m01,
            self.m11,
            self.m21,
            self.m31,

            self.m02,
            self.m12,
            self.m22,
            self.m32,

            self.m03,
            self.m13,
            self.m23,
            self.m33,
        )

    def inverse(self) -> Mat4:
        """
        Return the inverse using Gauss-Jordan elimination.

        Raises:
            ValueError: if the matrix is not invertible.
        """

        rows = [
            [
                self.m00,
                self.m01,
                self.m02,
                self.m03,
                1.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                self.m10,
                self.m11,
                self.m12,
                self.m13,
                0.0,
                1.0,
                0.0,
                0.0,
            ],
            [
                self.m20,
                self.m21,
                self.m22,
                self.m23,
                0.0,
                0.0,
                1.0,
                0.0,
            ],
            [
                self.m30,
                self.m31,
                self.m32,
                self.m33,
                0.0,
                0.0,
                0.0,
                1.0,
            ],
        ]

        for column in range(4):
            pivot = max(
                range(column, 4),
                key=lambda row: abs(rows[row][column]),
            )

            pivot_value = rows[pivot][column]

            if math.isclose(
                pivot_value,
                0.0,
                abs_tol=1e-12,
            ):
                raise ValueError("Matrix is not invertible")

            rows[column], rows[pivot] = rows[pivot], rows[column]

            pivot_value = rows[column][column]

            for j in range(8):
                rows[column][j] /= pivot_value

            for row in range(4):
                if row == column:
                    continue

                factor = rows[row][column]

                if factor == 0.0:
                    continue

                for j in range(8):
                    rows[row][j] -= factor * rows[column][j]

        return Mat4(
            rows[0][4],
            rows[0][5],
            rows[0][6],
            rows[0][7],

            rows[1][4],
            rows[1][5],
            rows[1][6],
            rows[1][7],

            rows[2][4],
            rows[2][5],
            rows[2][6],
            rows[2][7],

            rows[3][4],
            rows[3][5],
            rows[3][6],
            rows[3][7],
        )