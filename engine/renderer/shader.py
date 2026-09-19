from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class Shader:

    def __init__(self, vertex_path: str, fragment_path: str) -> None:
        with open(vertex_path, "r") as file:
            vertex_source = file.read()

        with open(fragment_path, "r") as file:
            fragment_source = file.read()

        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_source)
        glCompileShader(vertex_shader)

        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader)
            raise RuntimeError(error.decode())

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_source)
        glCompileShader(fragment_shader)

        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader)
            raise RuntimeError(error.decode())

        self.program = glCreateProgram()

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.program)
            raise RuntimeError(error.decode())

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)


    def use(self) -> None:
        glUseProgram(self.program)
        

    def destroy(self) -> None:
        if self.program:
            glDeleteProgram(self.program)
            self.program = 0