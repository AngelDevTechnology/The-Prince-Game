from __future__ import annotations

from dataclasses import dataclass
import math

from .vector3D import Vec3


@dataclass(slots=True)
class Mat3:
    """
    3x3 matrix.

    Convention:
    - row-major storage
    - column vectors
    - M @ v
    - transformations are applied right-to-left

    Mainly used for:
    - rotations
    - directions
    - normals
    - bases
    - extracting the linear part of a Mat4
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

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def identity(cls) -> Mat3:
        return cls(
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        )

    @classmethod
    def rotation_x(cls, angle: float) -> Mat3:
        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            1.0, 0.0, 0.0,
            0.0, c, -s,
            0.0, s, c,
        )

    @classmethod
    def rotation_y(cls, angle: float) -> Mat3:
        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, 0.0, s,
            0.0, 1.0, 0.0,
            -s, 0.0, c,
        )

    @classmethod
    def rotation_z(cls, angle: float) -> Mat3:
        c = math.cos(angle)
        s = math.sin(angle)

        return cls(
            c, -s, 0.0,
            s, c, 0.0,
            0.0, 0.0, 1.0,
        )

    @classmethod
    def from_mat4(cls, matrix) -> Mat3:
        """
        Extract the upper-left 3x3 linear part of a Mat4.

        Translation is ignored.
        """

        return cls(
            matrix.m00,
            matrix.m01,
            matrix.m02,

            matrix.m10,
            matrix.m11,
            matrix.m12,

            matrix.m20,
            matrix.m21,
            matrix.m22,
        )

    # ------------------------------------------------------------------
    # Multiplication
    # ------------------------------------------------------------------

    def __matmul__(self, other: Mat3 | Vec3) -> Mat3 | Vec3:

        # --------------------------------------------------------------
        # Mat3 @ Vec3
        # --------------------------------------------------------------

        if isinstance(other, Vec3):
            x = other.x
            y = other.y
            z = other.z

            return Vec3(
                self.m00 * x
                + self.m01 * y
                + self.m02 * z,

                self.m10 * x
                + self.m11 * y
                + self.m12 * z,

                self.m20 * x
                + self.m21 * y
                + self.m22 * z,
            )

        # --------------------------------------------------------------
        # Mat3 @ Mat3
        # --------------------------------------------------------------

        if isinstance(other, Mat3):
            a00, a01, a02 = (
                self.m00,
                self.m01,
                self.m02,
            )
            a10, a11, a12 = (
                self.m10,
                self.m11,
                self.m12,
            )
            a20, a21, a22 = (
                self.m20,
                self.m21,
                self.m22,
            )

            b00, b01, b02 = (
                other.m00,
                other.m01,
                other.m02,
            )
            b10, b11, b12 = (
                other.m10,
                other.m11,
                other.m12,
            )
            b20, b21, b22 = (
                other.m20,
                other.m21,
                other.m22,
            )

            return Mat3(
                a00 * b00 + a01 * b10 + a02 * b20,
                a00 * b01 + a01 * b11 + a02 * b21,
                a00 * b02 + a01 * b12 + a02 * b22,

                a10 * b00 + a11 * b10 + a12 * b20,
                a10 * b01 + a11 * b11 + a12 * b21,
                a10 * b02 + a11 * b12 + a12 * b22,

                a20 * b00 + a21 * b10 + a22 * b20,
                a20 * b01 + a21 * b11 + a22 * b21,
                a20 * b02 + a21 * b12 + a22 * b22,
            )

        return NotImplemented

    # ------------------------------------------------------------------
    # Matrix operations
    # ------------------------------------------------------------------

    def transpose(self) -> Mat3:
        return Mat3(
            self.m00,
            self.m10,
            self.m20,

            self.m01,
            self.m11,
            self.m21,

            self.m02,
            self.m12,
            self.m22,
        )

    def determinant(self) -> float:
        return (
            self.m00 * (
                self.m11 * self.m22
                - self.m12 * self.m21
            )
            - self.m01 * (
                self.m10 * self.m22
                - self.m12 * self.m20
            )
            + self.m02 * (
                self.m10 * self.m21
                - self.m11 * self.m20
            )
        )

    def inverse(self) -> Mat3:
        """
        Return the inverse of the matrix.

        Raises:
            ValueError: if the matrix is not invertible.
        """

        determinant = self.determinant()

        if math.isclose(
            determinant,
            0.0,
            abs_tol=1e-12,
        ):
            raise ValueError("Matrix is not invertible")

        inv_determinant = 1.0 / determinant

        return Mat3(
            (
                self.m11 * self.m22
                - self.m12 * self.m21
            ) * inv_determinant,

            (
                self.m02 * self.m21
                - self.m01 * self.m22
            ) * inv_determinant,

            (
                self.m01 * self.m12
                - self.m02 * self.m11
            ) * inv_determinant,

            (
                self.m12 * self.m20
                - self.m10 * self.m22
            ) * inv_determinant,

            (
                self.m00 * self.m22
                - self.m02 * self.m20
            ) * inv_determinant,

            (
                self.m02 * self.m10
                - self.m00 * self.m12
            ) * inv_determinant,

            (
                self.m10 * self.m21
                - self.m11 * self.m20
            ) * inv_determinant,

            (
                self.m01 * self.m20
                - self.m00 * self.m21
            ) * inv_determinant,

            (
                self.m00 * self.m11
                - self.m01 * self.m10
            ) * inv_determinant,
        )

    # ------------------------------------------------------------------
    # Specialized operations
    # ------------------------------------------------------------------

    def transform_direction(self, direction: Vec3) -> Vec3:
        """
        Transform a direction vector.

        Translation does not apply to directions.
        """
        return self @ direction

    def normal_matrix(self) -> Mat3:
        """
        Return the normal matrix of this matrix.

        Formula:

            normal_matrix = inverse(M).transpose()
        """
        return self.inverse().transpose()
