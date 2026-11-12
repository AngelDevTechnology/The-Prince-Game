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
    """
    Représente un maillage 3D stocké dans la mémoire GPU.

    Chaque sommet contient :
        - Position : (x, y, z)
        - Normale  : (nx, ny, nz)

    Attributs OpenGL :
        - Location 0 : Position
        - Location 1 : Normale

    Le maillage peut utiliser :
        - Un dessin non indexé (glDrawArrays).
        - Un dessin indexé (glDrawElements).
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        vertices: np.ndarray | list[float],
        indices: np.ndarray | list[int] | None = None,
    ) -> None:
        """
        Initialise un maillage et crée ses ressources OpenGL.

        Args:
            vertices:
                Sommets sous forme de liste plate ou de tableau (N, 3).

            indices:
                Indices des triangles. None pour un maillage non indexé.
        """

        # --------------------------------------------------------
        # Geometry
        # --------------------------------------------------------

        self.positions = self._prepare_positions(vertices)
        self.index_data = self._prepare_indices(indices)

        # --------------------------------------------------------
        # Vertex attributes
        # --------------------------------------------------------

        self.normals = self._compute_normals()

        self.vertex_data = np.ascontiguousarray(
            np.concatenate(
                (self.positions, self.normals),
                axis=1,
            ),
            dtype=np.float32,
        )

        # --------------------------------------------------------
        # OpenGL resources
        # --------------------------------------------------------

        self.vao = 0
        self.vbo = 0
        self.ebo = 0

        self.destroyed = False

        self._create_buffers()

    # ============================================================
    # GEOMETRY PREPARATION
    # ============================================================

    @staticmethod
    def _prepare_positions(
        vertices: np.ndarray | list[float],
    ) -> np.ndarray:
        """
        Convertit les positions en tableau NumPy contigu.

        Formats acceptés :
            - [x, y, z, x, y, z, ...]
            - [[x, y, z], [x, y, z], ...]
        """

        positions = np.asarray(vertices, dtype=np.float32)

        if positions.ndim == 1:
            if positions.size % 3 != 0:
                raise ValueError(
                    "Vertices must contain groups of 3 floats."
                )

            positions = positions.reshape(-1, 3)

        elif positions.ndim != 2 or positions.shape[1] != 3:
            raise ValueError("Vertices must have shape (N, 3).")

        if len(positions) == 0:
            raise ValueError("A mesh must contain at least one vertex.")

        if not np.all(np.isfinite(positions)):
            raise ValueError("Vertices must contain finite values.")

        return np.ascontiguousarray(positions)

    def _prepare_indices(
        self,
        indices: np.ndarray | list[int] | None,
    ) -> np.ndarray | None:
        """
        Valide et prépare les indices des triangles.

        Chaque groupe de trois indices représente un triangle.
        """

        if indices is None:
            if len(self.positions) % 3 != 0:
                raise ValueError(
                    "Non-indexed meshes need a multiple of 3 vertices."
                )

            return None

        raw_indices = np.asarray(indices)

        if raw_indices.ndim != 1:
            raw_indices = raw_indices.reshape(-1)

        if raw_indices.size == 0:
            raise ValueError("Index data cannot be empty.")

        if raw_indices.size % 3 != 0:
            raise ValueError("Indices must contain groups of 3.")

        if not np.issubdtype(raw_indices.dtype, np.integer):
            raise ValueError("Indices must be integers.")

        if np.any(raw_indices < 0) or np.any(
            raw_indices >= len(self.positions)
        ):
            raise ValueError("Index references an invalid vertex.")

        return np.ascontiguousarray(raw_indices, dtype=np.uint32)

    # ============================================================
    # NORMAL GENERATION
    # ============================================================

    def _compute_normals(self) -> np.ndarray:
        """
        Calcule les normales des sommets à partir des triangles.

        Les normales des faces sont accumulées sur leurs sommets,
        puis normalisées.

        Cette méthode produit des normales lissées par sommet.
        """

        normals = np.zeros_like(self.positions)

        # Récupère les triangles selon le type de maillage.
        triangles = (
            self.index_data.reshape(-1, 3)
            if self.index_data is not None
            else np.arange(len(self.positions)).reshape(-1, 3)
        )

        # Accumule les normales des faces sur chaque sommet.
        for i0, i1, i2 in triangles:
            a = self.positions[i0]
            b = self.positions[i1]
            c = self.positions[i2]

            face_normal = np.cross(b - a, c - a)

            # Ignore les triangles dégénérés.
            if np.dot(face_normal, face_normal) <= 1e-16:
                continue

            normals[i0] += face_normal
            normals[i1] += face_normal
            normals[i2] += face_normal

        # Normalise les normales accumulées.
        lengths = np.linalg.norm(normals, axis=1)

        valid = lengths > 1e-8
        normals[valid] /= lengths[valid, None]

        # Évite les normales nulles.
        normals[~valid] = (0.0, 1.0, 0.0)

        return normals

    # ============================================================
    # OPENGL RESOURCE CREATION
    # ============================================================

    def _create_buffers(self) -> None:
        """
        Crée et configure les ressources OpenGL.

        VAO : mémorise la configuration des attributs.
        VBO : contient les données des sommets.
        EBO : contient les indices des triangles.
        """

        try:
            # ----------------------------------------------------
            # Generate OpenGL objects
            # ----------------------------------------------------

            self.vao = glGenVertexArrays(1)
            self.vbo = glGenBuffers(1)

            if self.index_data is not None:
                self.ebo = glGenBuffers(1)

            # ----------------------------------------------------
            # Bind Vertex Array Object
            # ----------------------------------------------------

            glBindVertexArray(self.vao)

            # ----------------------------------------------------
            # Upload vertex data
            # ----------------------------------------------------

            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

            glBufferData(
                GL_ARRAY_BUFFER,
                self.vertex_data.nbytes,
                self.vertex_data,
                GL_STATIC_DRAW,
            )

            stride = self.vertex_data.strides[0]

            # ----------------------------------------------------
            # Vertex Attribute 0 : Position
            # ----------------------------------------------------

            glVertexAttribPointer(
                0,
                3,
                GL_FLOAT,
                GL_FALSE,
                stride,
                ctypes.c_void_p(0),
            )

            glEnableVertexAttribArray(0)

            # ----------------------------------------------------
            # Vertex Attribute 1 : Normal
            # ----------------------------------------------------

            glVertexAttribPointer(
                1,
                3,
                GL_FLOAT,
                GL_FALSE,
                stride,
                ctypes.c_void_p(3 * self.vertex_data.itemsize),
            )

            glEnableVertexAttribArray(1)

            # ----------------------------------------------------
            # Upload index data
            # ----------------------------------------------------

            if self.index_data is not None:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)

                glBufferData(
                    GL_ELEMENT_ARRAY_BUFFER,
                    self.index_data.nbytes,
                    self.index_data,
                    GL_STATIC_DRAW,
                )

            # ----------------------------------------------------
            # Unbind OpenGL objects
            # ----------------------------------------------------

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)

        except Exception:
            self.destroy()
            raise

    # ============================================================
    # RENDERING
    # ============================================================

    def draw(self) -> None:
        """
        Dessine le maillage avec GL_TRIANGLES.

        Utilise glDrawElements si le maillage possède des indices,
        sinon utilise glDrawArrays.
        """

        if self.destroyed:
            raise RuntimeError("Cannot draw a destroyed mesh.")

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
                len(self.positions),
            )

        glBindVertexArray(0)

    # ============================================================
    # RESOURCE DESTRUCTION
    # ============================================================

    def destroy(self) -> None:
        """
        Libère les ressources OpenGL associées au maillage.

        Cette méthode doit être appelée avec un contexte OpenGL valide.
        Elle peut être appelée plusieurs fois sans supprimer deux fois
        les mêmes ressources.
        """

        if self.destroyed:
            return

        # --------------------------------------------------------
        # Delete Element Buffer Object
        # --------------------------------------------------------

        if self.ebo:
            glDeleteBuffers(1, [self.ebo])
            self.ebo = 0

        # --------------------------------------------------------
        # Delete Vertex Buffer Object
        # --------------------------------------------------------

        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
            self.vbo = 0

        # --------------------------------------------------------
        # Delete Vertex Array Object
        # --------------------------------------------------------

        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = 0

        self.destroyed = True
