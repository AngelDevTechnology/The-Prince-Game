from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from OpenGL.GL import (
    GL_FALSE,
    GL_FRAGMENT_SHADER,
    GL_TRUE,
    GL_VERTEX_SHADER,
    glDeleteProgram,
    glDeleteShader,
    glGetUniformLocation,
    glUniform1f,
    glUniform1i,
    glUniform1ui,
    glUniform2f,
    glUniform2i,
    glUniform3f,
    glUniform3i,
    glUniform4f,
    glUniform4i,
    glUniformMatrix2fv,
    glUniformMatrix3fv,
    glUniformMatrix4fv,
    glUseProgram,
)
from OpenGL.GL.shaders import compileProgram, compileShader

from engine.math3d.mat4d import Mat4

FloatMatrix = NDArray[np.float32]


class Shader:
    """
    Gère un programme shader OpenGL.

    Responsabilités :
        - Charger les sources vertex et fragment.
        - Compiler et linker les shaders.
        - Gérer le programme OpenGL.
        - Récupérer et mettre en cache les uniform locations.
        - Envoyer des données aux uniforms.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        vertex_path: str | Path,
        fragment_path: str | Path,
    ) -> None:
        """
        Initialise un programme shader à partir de deux fichiers.

        Args:
            vertex_path: Chemin du vertex shader.
            fragment_path: Chemin du fragment shader.
        """

        # --------------------------------------------------------
        # Shader paths
        # --------------------------------------------------------

        self.vertex_path = Path(vertex_path)
        self.fragment_path = Path(fragment_path)

        self._validate_path([
            self.vertex_path,
            self.fragment_path,
        ])

        # --------------------------------------------------------
        # Shader sources
        # --------------------------------------------------------

        self.vertex_source = self._read_source(self.vertex_path)
        self.fragment_source = self._read_source(self.fragment_path)

        # --------------------------------------------------------
        # OpenGL resources
        # --------------------------------------------------------

        self.program_id = self._compile()

        # Cache des uniform locations.
        self.uniform_locations: dict[str, int] = {}

    # ============================================================
    # SHADER SOURCE MANAGEMENT
    # ============================================================

    @staticmethod
    def _validate_path(file_paths: list[str | Path]) -> None:
        """
        Vérifie que tous les fichiers shaders existent.
        """

        for file in file_paths:
            path = Path(file)

            if not path.is_file():
                raise FileNotFoundError(
                    f"Shader file not found: {path}"
                )

    @staticmethod
    def _read_source(file_path: Path) -> str:
        """
        Lit le contenu d'un fichier shader.

        Raises:
            ValueError: Si le fichier est vide.
        """

        source = file_path.read_text(encoding="utf-8")

        if not source.strip():
            raise ValueError(
                f"Shader file is empty: {file_path}"
            )

        return source

    # ============================================================
    # SHADER COMPILATION
    # ============================================================

    def _compile(self) -> int:
        """
        Compile les shaders et crée le programme OpenGL.

        Étapes :
            1. Compilation du vertex shader.
            2. Compilation du fragment shader.
            3. Link des deux shaders dans un programme.
            4. Libération des objets shader temporaires.

        Returns:
            Identifiant du programme OpenGL.
        """

        vertex_shader = 0
        fragment_shader = 0

        try:
            # ----------------------------------------------------
            # Compile vertex shader
            # ----------------------------------------------------

            vertex_shader = compileShader(
                self.vertex_source,
                GL_VERTEX_SHADER,
            )

            # ----------------------------------------------------
            # Compile fragment shader
            # ----------------------------------------------------

            fragment_shader = compileShader(
                self.fragment_source,
                GL_FRAGMENT_SHADER,
            )

            # ----------------------------------------------------
            # Link shader program
            # ----------------------------------------------------

            program_id = int(
                compileProgram(
                    vertex_shader,
                    fragment_shader,
                )
            )

            return program_id

        finally:
            # ----------------------------------------------------
            # Delete temporary shader objects
            # ----------------------------------------------------

            if vertex_shader:
                glDeleteShader(vertex_shader)

            if fragment_shader:
                glDeleteShader(fragment_shader)

    # ============================================================
    # UNIFORM MANAGEMENT
    # ============================================================

    def _get_uniform_location(self, name: str) -> int:
        """
        Récupère la location d'un uniform.

        Les locations sont mises en cache pour éviter
        des appels répétés à glGetUniformLocation.

        Raises:
            RuntimeError: Si l'uniform n'existe pas ou est inactif.
        """

        if name not in self.uniform_locations:
            location = glGetUniformLocation(
                self.program_id,
                name,
            )

            if location == -1:
                raise RuntimeError(
                    f"Uniform '{name}' not found or inactive."
                )

            self.uniform_locations[name] = location

        return self.uniform_locations[name]

    # ============================================================
    # PROGRAM ACTIVATION
    # ============================================================

    def use(self) -> None:
        """
        Active le programme shader.
        """

        if not self.program_id:
            raise RuntimeError("Shader program has been deleted.")

        glUseProgram(self.program_id)

    # ============================================================
    # FLOAT UNIFORMS
    # ============================================================

    def set_float(self, name: str, value: float) -> None:
        """Envoie un float à un uniform."""

        location = self._get_uniform_location(name)
        glUniform1f(location, value)

    # ============================================================
    # INTEGER UNIFORMS
    # ============================================================

    def set_int(self, name: str, value: int) -> None:
        """Envoie un entier signé à un uniform."""

        location = self._get_uniform_location(name)
        glUniform1i(location, value)

    def set_bool(self, name: str, value: bool) -> None:
        """Envoie un booléen à un uniform."""

        location = self._get_uniform_location(name)
        glUniform1i(location, int(value))

    def set_uint(self, name: str, value: int) -> None:
        """Envoie un entier non signé à un uniform."""

        if value < 0:
            raise ValueError("Unsigned uniform cannot be negative.")

        location = self._get_uniform_location(name)
        glUniform1ui(location, value)

    # ============================================================
    # FLOAT VECTOR UNIFORMS
    # ============================================================

    def set_vec2(
        self,
        name: str,
        value: tuple[float, float],
    ) -> None:
        """Envoie un vec2 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform2f(location, *value)

    def set_vec3(
        self,
        name: str,
        value: tuple[float, float, float],
    ) -> None:
        """Envoie un vec3 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform3f(location, *value)

    def set_vec4(
        self,
        name: str,
        value: tuple[float, float, float, float],
    ) -> None:
        """Envoie un vec4 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform4f(location, *value)

    # ============================================================
    # INTEGER VECTOR UNIFORMS
    # ============================================================

    def set_ivec2(
        self,
        name: str,
        value: tuple[int, int],
    ) -> None:
        """Envoie un ivec2 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform2i(location, *value)

    def set_ivec3(
        self,
        name: str,
        value: tuple[int, int, int],
    ) -> None:
        """Envoie un ivec3 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform3i(location, *value)

    def set_ivec4(
        self,
        name: str,
        value: tuple[int, int, int, int],
    ) -> None:
        """Envoie un ivec4 à un uniform."""

        location = self._get_uniform_location(name)
        glUniform4i(location, *value)

    # ============================================================
    # MATRIX UNIFORMS
    # ============================================================

    def set_mat2(self, name: str, value: FloatMatrix) -> None:
        """Envoie une matrice 2x2 à un uniform."""

        value = np.ascontiguousarray(value, dtype=np.float32)

        if value.shape != (2, 2):
            raise ValueError("Expected a 2x2 matrix.")

        location = self._get_uniform_location(name)

        glUniformMatrix2fv(
            location,
            1,
            GL_FALSE,
            value,
        )

    def set_mat3(self, name: str, value: FloatMatrix) -> None:
        """Envoie une matrice 3x3 à un uniform."""

        value = np.ascontiguousarray(value, dtype=np.float32)

        if value.shape != (3, 3):
            raise ValueError("Expected a 3x3 matrix.")

        location = self._get_uniform_location(name)

        glUniformMatrix3fv(
            location,
            1,
            GL_FALSE,
            value,
        )

    def set_mat4(self, name: str, matrix: Mat4) -> None:
        """
        Envoie une Mat4 personnalisée à un uniform.

        La classe Mat4 utilise :
            - Un stockage row-major.
            - Des vecteurs colonnes.

        GL_TRUE demande à OpenGL de transposer les données
        lors de leur interprétation.
        """

        location = self._get_uniform_location(name)

        value = np.array(
            [
                matrix.m00, matrix.m01, matrix.m02, matrix.m03,
                matrix.m10, matrix.m11, matrix.m12, matrix.m13,
                matrix.m20, matrix.m21, matrix.m22, matrix.m23,
                matrix.m30, matrix.m31, matrix.m32, matrix.m33,
            ],
            dtype=np.float32,
        )

        glUniformMatrix4fv(
            location,
            1,
            GL_TRUE,
            value,
        )

    # ============================================================
    # RESOURCE DESTRUCTION
    # ============================================================

    def delete(self) -> None:
        """
        Supprime le programme OpenGL et vide le cache des uniforms.

        Cette méthode peut être appelée plusieurs fois.
        """

        if self.program_id:
            glDeleteProgram(self.program_id)
            self.program_id = 0

        self.uniform_locations.clear()
