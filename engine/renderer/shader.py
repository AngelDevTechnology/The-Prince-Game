from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class Shader:

    def __init__(self, vertex_path: str, fragment_path: str) -> None:
        with open(vertex_path) as file:
            vertex_source = file.read()

        with open(fragment_path) as file:
            fragment_source = file.read()


        vertex_shader = compileShader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_source, GL_FRAGMENT_SHADER)

        self.program = compileProgram(vertex_shader, fragment_shader)


    def use(self) -> None:
        glUseProgram(self.program)


    def destroy(self) -> None:
        glDeleteProgram(self.program)