from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Quaternion:
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def normalized(self):
        norm = np.linalg.norm([self.w, self.x, self.y, self.z])
        if norm == 0:
            raise ValueError("Impossible de normaliser un quaternion nul")

        return Quaternion(self.w / norm, self.x / norm, self.y / norm, self.z / norm)

    def __mul__(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    @staticmethod
    def from_axis_angle(
        axis: tuple[float, float, float], angle_rad: float
    ) -> Quaternion:
        axis_array = np.asarray(axis, dtype=np.float64)
        norm = np.linalg.norm(axis_array)

        if norm < 1e-8:
            raise ValueError("Rotation axis cannot be zero.")

        axis_array /= norm
        half = angle_rad / 2.0
        s = np.sin(half)

        return Quaternion(
            float(np.cos(half)),
            float(axis_array[0] * s),
            float(axis_array[1] * s),
            float(axis_array[2] * s),
        )

    def rotate_vector(self, vector: tuple[float, float, float]) -> np.ndarray:
        q = self.normalized()
        v = np.asarray(vector, dtype=np.float64)

        qv = np.array([q.x, q.y, q.z])
        t = 2.0 * np.cross(qv, v)

        return v + q.w * t + np.cross(qv, t)

    def to_matrix(self) -> np.ndarray:
        q = self.normalized()

        w, x, y, z = q.w, q.x, q.y, q.z

        return np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ],
            dtype=np.float32,
        )
