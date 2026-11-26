from __future__ import annotations

import math
from dataclasses import dataclass

from .mat3d import Mat3
from .vector3d import Vec3


@dataclass(slots=True)
class Quaternion:
    """
    Quaternion used to represent 3D rotations.

    Component order: (w, x, y, z).
    Uses Hamilton multiplication and right-handed rotations.
    """

    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    # --------------------------------------------------
    # Arithmetic
    # --------------------------------------------------

    def __mul__(self, other: Quaternion) -> Quaternion:
        """Hamilton product."""
        return Quaternion(
            self.w * other.w - self.x * other.x
            - self.y * other.y - self.z * other.z,

            self.w * other.x + self.x * other.w
            + self.y * other.z - self.z * other.y,

            self.w * other.y - self.x * other.z
            + self.y * other.w + self.z * other.x,

            self.w * other.z + self.x * other.y
            - self.y * other.x + self.z * other.w,
        )

    def __add__(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __neg__(self) -> Quaternion:
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __mul_scalar(self, scalar: float) -> Quaternion:
        return Quaternion(
            self.w * scalar,
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    # --------------------------------------------------
    # Length and normalization
    # --------------------------------------------------

    def length_squared(self) -> float:
        return (
            self.w**2
            + self.x**2
            + self.y**2
            + self.z**2
        )

    def length(self) -> float:
        return math.hypot(self.w, self.x, self.y, self.z)

    def normalized(self) -> Quaternion:
        magnitude = self.length()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero quaternion")

        return Quaternion(
            self.w / magnitude,
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude,
        )

    def normalize(self) -> None:
        magnitude = self.length()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero quaternion")

        self.w /= magnitude
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude

    # --------------------------------------------------
    # Quaternion operations
    # --------------------------------------------------

    def dot(self, other: Quaternion) -> float:
        return (
            self.w * other.w
            + self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )

    def conjugate(self) -> Quaternion:
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> Quaternion:
        magnitude_squared = self.length_squared()

        if magnitude_squared == 0:
            raise ValueError("Cannot invert a zero quaternion")

        conjugate = self.conjugate()

        return Quaternion(
            conjugate.w / magnitude_squared,
            conjugate.x / magnitude_squared,
            conjugate.y / magnitude_squared,
            conjugate.z / magnitude_squared,
        )

    # --------------------------------------------------
    # Construction
    # --------------------------------------------------

    @classmethod
    def from_axis_angle(
        cls,
        axis: Vec3,
        angle_rad: float,
    ) -> Quaternion:
        magnitude = axis.length()

        if magnitude < 1e-8:
            raise ValueError("Rotation axis cannot be zero")

        half_angle = angle_rad * 0.5
        sine = math.sin(half_angle)

        return cls(
            math.cos(half_angle),
            axis.x / magnitude * sine,
            axis.y / magnitude * sine,
            axis.z / magnitude * sine,
        )

    @classmethod
    def from_euler(
        cls,
        pitch: float,
        yaw: float,
        roll: float,
    ) -> Quaternion:
        """
        Create a quaternion from Euler angles.

        Convention: yaw (Y), pitch (X), roll (Z).
        Composition: q_yaw * q_pitch * q_roll.
        """
        q_pitch = cls.from_axis_angle(
            Vec3(1.0, 0.0, 0.0), pitch
        )
        q_yaw = cls.from_axis_angle(
            Vec3(0.0, 1.0, 0.0), yaw
        )
        q_roll = cls.from_axis_angle(
            Vec3(0.0, 0.0, 1.0), roll
        )

        return (q_yaw * q_pitch * q_roll).normalized()

    # --------------------------------------------------
    # Vector rotation
    # --------------------------------------------------

    def rotate_vector(self, vector: Vec3) -> Vec3:
        """
        Rotate a vector using q * v * q^-1.

        The quaternion is normalized before rotation.
        """
        q = self.normalized()

        q_vector = Vec3(q.x, q.y, q.z)

        t = q_vector.cross(vector) * 2.0

        return vector + t * q.w + q_vector.cross(t)

    # --------------------------------------------------
    # Matrix conversion
    # --------------------------------------------------

    def to_mat3(self) -> Mat3:
        q = self.normalized()

        w, x, y, z = q.w, q.x, q.y, q.z

        return Mat3(
            1 - 2 * (y * y + z * z),
            2 * (x * y - z * w),
            2 * (x * z + y * w),

            2 * (x * y + z * w),
            1 - 2 * (x * x + z * z),
            2 * (y * z - x * w),

            2 * (x * z - y * w),
            2 * (y * z + x * w),
            1 - 2 * (x * x + y * y),
        )

    # --------------------------------------------------
    # Interpolation
    # --------------------------------------------------

    @staticmethod
    def slerp(
        start: Quaternion,
        end: Quaternion,
        t: float,
    ) -> Quaternion:
        """
        Spherical linear interpolation between two rotations.
        """
        q1 = start.normalized()
        q2 = end.normalized()

        dot = q1.dot(q2)

        # Use the shortest rotational path.
        if dot < 0.0:
            q2 = -q2
            dot = -dot

        dot = max(-1.0, min(1.0, dot))

        # Nearly identical rotations: use linear interpolation.
        if dot > 0.9995:
            result = q1 + (q2 - q1).__mul_scalar(t)
            return result.normalized()

        theta = math.acos(dot)
        sin_theta = math.sin(theta)

        weight1 = math.sin((1.0 - t) * theta) / sin_theta
        weight2 = math.sin(t * theta) / sin_theta

        return (
            q1.__mul_scalar(weight1)
            + q2.__mul_scalar(weight2)
        ).normalized()

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def copy(self) -> Quaternion:
        return Quaternion(self.w, self.x, self.y, self.z)
