from __future__ import annotations

import ctypes

import numpy as np
from OpenGL.GL import *


class Mesh:
    def __init__(self, vertices: list[float], indices: list[int] | None = None) -> None:
        if len(vertices) % 3 != 0:
            raise ValueError("Vertices must contain groups of 3 floats (x, y, z).")

        self.positions = np.asarray(vertices, dtype=np.float32).reshape(-1, 3)

        if indices is None:
            if len(self.positions) % 3 != 0:
                raise ValueError("Non-indexed meshes need a multiple of 3 vertices.")
            self.index_data = None
        else:
            if len(indices) % 3 != 0:
                raise ValueError("Indices must contain groups of 3 for GL_TRIANGLES.")
            if any(index < 0 or index >= len(self.positions) for index in indices):
                raise ValueError("Every index must refer to an existing vertex.")
            self.index_data = np.asarray(indices, dtype=np.uint32)

        self.normals = self._compute_normals()
        # Interleaved data: position (xyz) followed by normal (xyz).
        self.vertex_data = np.ascontiguousarray(
            np.concatenate((self.positions, self.normals), axis=1),
            dtype=np.float32,
        )

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1) if self.index_data is not None else None

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, GL_STATIC_DRAW)

        stride = 6 * self.vertex_data.itemsize

        # Attribute 0: position (first 3 floats of each vertex).
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Attribute 1: normal (next 3 floats of each vertex).
        glVertexAttribPointer(
            1, 3, GL_FLOAT, GL_FALSE, stride,
            ctypes.c_void_p(3 * self.vertex_data.itemsize),
        )
        glEnableVertexAttribArray(1)

        if self.index_data is not None:
            # The element buffer binding is stored in the VAO.
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                self.index_data.nbytes,
                self.index_data,
                GL_STATIC_DRAW,
            )

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def _compute_normals(self) -> np.ndarray:
        normals = np.zeros_like(self.positions)

        triangles = (
            self.index_data.reshape(-1, 3)
            if self.index_data is not None
            else np.arange(len(self.positions)).reshape(-1, 3)
        )

        for i0, i1, i2 in triangles:
            a, b, c = self.positions[[i0, i1, i2]]
            face_normal = np.cross(b - a, c - a)
            normals[i0] += face_normal
            normals[i1] += face_normal
            normals[i2] += face_normal

        lengths = np.linalg.norm(normals, axis=1)
        valid = lengths > 1e-8
        normals[valid] /= lengths[valid, None]
        return normals

    def draw(self) -> None:
        glBindVertexArray(self.vao)

        if self.index_data is not None:
            glDrawElements(GL_TRIANGLES, len(self.index_data), GL_UNSIGNED_INT, None)
        else:
            # vertex_data has one row per vertex, not one row per 3 vertices.
            glDrawArrays(GL_TRIANGLES, 0, len(self.positions))

        glBindVertexArray(0)

    def destroy(self) -> None:
        if self.ebo is not None:
            glDeleteBuffers(1, [self.ebo])
            self.ebo = None

        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
            self.vbo = 0

        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = 0
