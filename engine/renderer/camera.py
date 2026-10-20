
from __future__ import annotations
import glfw
import numpy as np
import math
from engine.math3d.quaternion import Quaternion
from engine.math3d.mat4D import Mat4


class Camera:
    def __init__(self, position=(0.0, 0.0, 3.0), fov=60.0, near=0.1, far=1000.0,):
        if not 0.0 < fov < 180.0:
            raise ValueError("fov must be between 0 and 180 degrees.")
        if not 0.0 < near < far:
            raise ValueError("Require 0 < near < far.")

        self.position = np.asarray(position, dtype=np.float32)
        self.orientation = Quaternion()
        self.fov = fov
        self.near = near
        self.far = far

        self.yaw = -90.0
        self.pitch = 0.0

        self.sensitivity = 0.1

        self.first_mouse = True
        self.last_x = 0.0
        self.last_y = 0.0

    def get_view_matrix(self) -> Mat4:
        rotation = self.orientation.to_matrix().T
        view = np.eye(4, dtype=np.float32)
        view[:3, :3] = rotation
        view[:3, 3] = -rotation @ self.position
        return Mat4(*view.flatten().tolist())


    def get_projection_matrix(self, aspect_ratio: float) -> Mat4:
        return Mat4.perspective(math.radians(self.fov), aspect_ratio, self.near, self.far)

    def rotate(self, axis: tuple[float, float, float], angle_rad: float) -> None:
        delta = Quaternion.from_axis_angle(axis, angle_rad)

        self.orientation = (delta * self.orientation).normalized()


    def update_orientation(self) -> None:
        yaw_q = Quaternion.from_axis_angle((0.0, 1.0, 0.0), np.radians(self.yaw))

        pitch_q = Quaternion.from_axis_angle((1.0, 0.0, 0.0), np.radians(self.pitch))

        self.orientation = (yaw_q * pitch_q).normalized()


    def handle_mouse(self, window, xpos: float, ypos: float) -> None:
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
        self.pitch -= dy * self.sensitivity

        self.pitch = float(np.clip(self.pitch, -89.0, 89.0))

        self.update_orientation()
