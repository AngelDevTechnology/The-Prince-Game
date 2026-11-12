from __future__ import annotations

import math

from engine.math3d.mat4d import Mat4
from engine.math3d.quaternion import Quaternion
from engine.math3d.vector3d import Vec3


class Camera:
    """
    3D perspective camera.

    Uses:
        - Right-handed coordinate system.
        - Camera forward direction: -Z.
        - Column vectors.
        - Quaternion-based orientation.
    """

    def __init__(
        self,
        position: Vec3 | None = None,
        fov: float = 60.0,
        near: float = 0.1,
        far: float = 1000.0,
    ) -> None:

        if not 0.0 < fov < 180.0:
            raise ValueError("FOV must be between 0 and 180 degrees.")

        if not 0.0 < near < far:
            raise ValueError("Require 0 < near < far.")

        self.position = position.copy() if position else Vec3(0.0, 0.0, 3.0)
        self.orientation = Quaternion()

        self.fov = fov
        self.near = near
        self.far = far

        # Euler angles, expressed in degrees.
        self.yaw = -90.0
        self.pitch = 0.0

        self.sensitivity = 0.1

        # Mouse state.
        self.first_mouse = True
        self.cursor_captured = True

        self.last_x = 0.0
        self.last_y = 0.0

    # --------------------------------------------------
    # View matrix
    # --------------------------------------------------

    def get_view_matrix(self) -> Mat4:
        """
        Build the inverse camera transformation.

        View = R^-1 * T^-1
        """

        rotation = self.orientation.conjugate().normalized().to_mat3()

        # Camera translation in view space.
        translated_position = rotation @ (-self.position)

        return Mat4(
            rotation.m00, rotation.m01, rotation.m02, translated_position.x,
            rotation.m10, rotation.m11, rotation.m12, translated_position.y,
            rotation.m20, rotation.m21, rotation.m22, translated_position.z,
            0.0, 0.0, 0.0, 1.0,
        )

    # --------------------------------------------------
    # Projection matrix
    # --------------------------------------------------

    def get_projection_matrix(self, aspect_ratio: float) -> Mat4:
        if aspect_ratio <= 0.0:
            raise ValueError("Aspect ratio must be positive.")

        return Mat4.perspective(
            math.radians(self.fov),
            aspect_ratio,
            self.near,
            self.far,
        )

    # --------------------------------------------------
    # Rotation
    # --------------------------------------------------

    def rotate(self, axis: Vec3, angle_rad: float) -> None:
        delta = Quaternion.from_axis_angle(axis, angle_rad)

        self.orientation = (
            delta * self.orientation
        ).normalized()

    def update_orientation(self) -> None:
        yaw_q = Quaternion.from_axis_angle(
            Vec3(0.0, 1.0, 0.0),
            math.radians(self.yaw),
        )

        pitch_q = Quaternion.from_axis_angle(
            Vec3(1.0, 0.0, 0.0),
            math.radians(self.pitch),
        )

        self.orientation = (
            yaw_q * pitch_q
        ).normalized()

    # --------------------------------------------------
    # Mouse input
    # --------------------------------------------------

    def handle_mouse(self, _window, xpos: float, ypos: float) -> None:

        if not self.cursor_captured:
            self.first_mouse = True
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
            return

        dx = xpos - self.last_x
        dy = ypos - self.last_y

        self.last_x = xpos
        self.last_y = ypos

        self.yaw -= dx * self.sensitivity

        self.pitch = max(
            -89.0,
            min(89.0, self.pitch - dy * self.sensitivity),
        )

        self.update_orientation()

    # --------------------------------------------------
    # Direction vectors
    # --------------------------------------------------

    def get_forward(self) -> Vec3:
        return self.orientation.rotate_vector(
            Vec3(0.0, 0.0, -1.0)
        ).normalized()

    def get_right(self) -> Vec3:
        return self.orientation.rotate_vector(
            Vec3(1.0, 0.0, 0.0)
        ).normalized()

    def get_up(self) -> Vec3:
        return self.orientation.rotate_vector(
            Vec3(0.0, 1.0, 0.0)
        ).normalized()

    # --------------------------------------------------
    # Movement
    # --------------------------------------------------

    def move(self, direction: Vec3, amount: float) -> None:
        self.position += direction * amount

    def move_forward(self, amount: float) -> None:
        self.move(self.get_forward(), amount)

    def move_right(self, amount: float) -> None:
        self.move(self.get_right(), amount)

    def move_up(self, amount: float) -> None:
        self.move(Vec3(0.0, 1.0, 0.0), amount)
