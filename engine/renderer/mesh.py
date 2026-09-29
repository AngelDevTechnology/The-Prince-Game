import ctypes
import numpy as np
from OpenGL.GL import *


class Mesh:
    def __init__(
        self,
        vertices: list[float],
        indices: list[int] | None = None,
    ) -> None:
        if len(vertices) % 3 != 0:
            raise ValueError(
                "Vertices must contain groups of 3 floats (x, y, z)."
            )

        self.vertex_data = np.array(vertices, dtype=np.float32)

        self.index_data = (
            np.array(indices, dtype=np.uint32)
            if indices is not None
            else None
        )

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        self.ebo = (
            glGenBuffers(1)
            if self.index_data is not None
            else None
        )

        glBindVertexArray(self.vao)

        # Vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.vertex_data.nbytes,
            self.vertex_data,
            GL_STATIC_DRAW,
        )

        # Position attribute
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            3 * self.vertex_data.itemsize,
            ctypes.c_void_p(0),
        )
        glEnableVertexAttribArray(0)

        # Index buffer
        if self.index_data is not None:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                self.index_data.nbytes,
                self.index_data,
                GL_STATIC_DRAW,
            )

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)

        if self.index_data is not None:
            glDrawElements(
                GL_TRIANGLES,
                len(self.index_data),
                GL_UNSIGNED_INT,
                None,
            )
        else:
            glDrawArrays(
                GL_TRIANGLES,
                0,
                len(self.vertex_data) // 3,
            )

        glBindVertexArray(0)

    def destroy(self) -> None:
        if self.ebo is not None:
            glDeleteBuffers(1, [self.ebo])

        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])