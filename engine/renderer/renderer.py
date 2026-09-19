from __future__ import annotations

from OpenGL.GL import *

from .mesh import Mesh
from .shader import Shader


class Renderer:
    """Owns global render state and issues draw calls."""

    def __init__(self) -> None:
        self._configure_state()

    @staticmethod
    def _configure_state() -> None:
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

        glClearColor(0.05, 0.05, 0.07, 1.0)

    @staticmethod
    def clear() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def draw(shader: Shader, mesh: Mesh) -> None:
        shader.use()
        mesh.draw()