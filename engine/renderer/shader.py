from __future__ import annotations

from pathlib import Path

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

import numpy as np
from numpy.typing import NDArray

FloatMatrix = NDArray[np.float32]


class Shader:
    """"""
    def __init__(self, vertex_path: str | Path, fragment_path: str | Path) -> None:
        Shader._validate_path([vertex_path, fragment_path])

        self.vertex_path: Path = Path(vertex_path)
        self.fragment_path: Path = Path(fragment_path)

        self.vertex_source: str = Shader._read_source(self.vertex_path)
        self.fragment_source: str = Shader._read_source(self.fragment_path)

        self.program_id: int = self._compile()
        self.uniform_locations: dict[str, int] = {}


    @staticmethod
    def _validate_path(file_paths: list[str | Path]) -> None:
        for file in file_paths:
            path = Path(file)

            if not path.is_file():
                raise FileNotFoundError(f"The file '{path}' was not found or is not a file.")


    @staticmethod
    def _read_source(file_path: Path) -> str:
        file_source: str = file_path.read_text(encoding="utf-8")

        if not file_source.strip():
            raise ValueError(f"The file '{file_path}' is empty.")

        return file_source


    def _compile(self) -> int:
        vertex_shader = 0
        fragment_shader = 0
        program_id = 0

        try:
            vertex_shader = compileShader(self.vertex_source, GL_VERTEX_SHADER)
            fragment_shader = compileShader(self.fragment_source, GL_FRAGMENT_SHADER)
            program_id = int(compileProgram(vertex_shader, fragment_shader))

            return program_id

        except Exception:
            if program_id:
                glDeleteProgram(program_id)
            raise

        finally:
            if vertex_shader:
                glDeleteShader(vertex_shader)

            if fragment_shader:
                glDeleteShader(fragment_shader)


    def _get_uniform_location(self, name: str) -> int:
        if name not in self.uniform_locations:
            location = glGetUniformLocation(self.program_id, name)

            if location == -1:
                raise RuntimeError(f"Uniform '{name}' not found")
            self.uniform_locations[name] = location

        return self.uniform_locations[name]


    def use(self) -> None:
        glUseProgram(self.program_id)


    def delete(self) -> None:
        if self.program_id != 0:
            glDeleteProgram(self.program_id)
            self.program_id = 0

        self.uniform_locations.clear()



    def set_float(self, name: str, value: float) -> None:
        location = self._get_uniform_location(name)
        glUniform1f(location, value)
    
    
    def set_int(self, name: str, value: int) -> None:
        location = self._get_uniform_location(name)
        glUniform1i(location, value)


    def set_bool(self, name: str, value: bool) -> None:
        location = self._get_uniform_location(name)
        glUniform1i(location, int(value))


    def set_uint(self, name: str, value: int) -> None:
        location = self._get_uniform_location(name)
        glUniform1ui(location, value)


    def set_vec2(self, name: str, value: tuple[float, float]) -> None:
        location = self._get_uniform_location(name)
        glUniform2f(location, *value)


    def set_vec3(self, name: str, value: tuple[float, float, float]) -> None:
        location = self._get_uniform_location(name)
        glUniform3f(location, *value)


    def set_vec4(self, name: str, value: tuple[float, float, float, float]) -> None:
        location = self._get_uniform_location(name)
        glUniform4f(location, *value)


    def set_ivec2(self, name: str, value: tuple[int, int]) -> None:
        location = self._get_uniform_location(name)
        glUniform2i(location, *value)


    def set_ivec3(self, name: str, value: tuple[int, int, int]) -> None:
        location = self._get_uniform_location(name)
        glUniform3i(location, *value)


    def set_ivec4(self, name: str, value: tuple[int, int, int, int]) -> None:
        location = self._get_uniform_location(name)
        glUniform4i(location, *value)


    def set_mat2(self, name: str, value: FloatMatrix) -> None:
        location = self._get_uniform_location(name)
        glUniformMatrix2fv(location, 1, GL_FALSE, value)


    def set_mat3(self, name: str, value: FloatMatrix) -> None:
        location = self._get_uniform_location(name)
        glUniformMatrix3fv(location, 1, GL_FALSE, value)


    def set_mat4(self, name: str, value: FloatMatrix) -> None:
        location = self._get_uniform_location(name)
        glUniformMatrix4fv(location, 1, GL_FALSE, value)