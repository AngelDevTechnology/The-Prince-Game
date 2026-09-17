import ctypes

import numpy as np
from OpenGL.GL import *


class Mesh:

    def __init__(self, vertices: list[float]) -> None:
        self.vertex_data = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertex_data.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def draw(self) -> None:
        glBindVertexArray(self.vao)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_data) // 3)
        glBindVertexArray(0)


    def destroy(self) -> None:
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])