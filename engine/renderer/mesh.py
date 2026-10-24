from __future__ import annotations

import ctypes

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glDeleteBuffers,
    glDeleteVertexArrays,
    glDrawArrays,
    glDrawElements,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glVertexAttribPointer,
)


class Mesh:
    def __init__(
        self,
        vertices: np.ndarray | list[float],
        indices: np.ndarray | list[int] | None = None,
    ) -> None:
        # Accepte une liste plate ou un tableau de forme (N, 3).
        positions = np.asarray(vertices, dtype=np.float32)

        if positions.ndim == 1:
            if positions.size % 3 != 0:
                raise ValueError("Vertices must contain groups of 3 floats (x, y, z).")
            positions = positions.reshape(-1, 3)
        elif positions.ndim != 2 or positions.shape[1] != 3:
            raise ValueError("Vertices must have shape (N, 3).")

        if len(positions) == 0:
            raise ValueError("A mesh must contain at least one vertex.")

        self.positions = np.ascontiguousarray(positions)

        # Prépare les indices des triangles.
        if indices is None:
            if len(self.positions) % 3 != 0:
                raise ValueError("Non-indexed meshes need a multiple of 3 vertices.")
            self.index_data = None
        else:
            raw_indices = np.asarray(indices)

            if raw_indices.ndim != 1:
                raw_indices = raw_indices.reshape(-1)

            if raw_indices.size % 3 != 0:
                raise ValueError("Indices must contain groups of 3 for GL_TRIANGLES.")

            if not np.issubdtype(raw_indices.dtype, np.integer):
                raise ValueError("Indices must be integers.")

            if np.any(raw_indices < 0) or np.any(raw_indices >= len(self.positions)):
                raise ValueError("Every index must refer to an existing vertex.")

            self.index_data = np.ascontiguousarray(raw_indices, dtype=np.uint32)

        # Calcule les normales pour l'éclairage.
        self.normals = self._compute_normals()

        # Chaque sommet contient : position (xyz) + normale (xyz).
        self.vertex_data = np.ascontiguousarray(
            np.concatenate((self.positions, self.normals), axis=1), dtype=np.float32
        )

        # Crée les buffers OpenGL.
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1) if self.index_data is not None else None

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, GL_STATIC_DRAW
        )

        stride = 6 * self.vertex_data.itemsize

        # Attribut 0 : position (xyz).
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Attribut 1 : normale (xyz).
        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            stride,
            ctypes.c_void_p(3 * self.vertex_data.itemsize),
        )
        glEnableVertexAttribArray(1)

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
