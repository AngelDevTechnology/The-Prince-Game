from __future__ import annotations

from OpenGL.GL import (
    GL_BACK,
    GL_CCW,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LESS,
    glClear,
    glClearColor,
    glCullFace,
    glDepthFunc,
    glEnable,
    glFrontFace,
)

from .mesh import Mesh
from .shader import Shader


class Renderer:
    """Owns global render state and issues draw calls."""

    def __init__(self) -> None:
        self._configure_state()

    @staticmethod
    def _configure_state() -> None:
        # Depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # Back-face culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

        # Clear color
        glClearColor(0.05, 0.05, 0.07, 1.0)

    @staticmethod
    def clear() -> None:
        glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))

    @staticmethod
    def draw(shader: Shader, mesh: Mesh) -> None:
        shader.use()
        mesh.draw()
