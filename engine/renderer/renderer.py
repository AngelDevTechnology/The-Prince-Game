from OpenGL.GL import *


class Renderer:

    def __init__(self, shader):
        self.shader = shader

        glClearColor(0.03, 0.03, 0.03, 1.0)


    def render(self, mesh) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        self.shader.use()
        mesh.draw()