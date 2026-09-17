from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT


class Renderer:
    def clear(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)


    def draw(self, shader, mesh) -> None:
        shader.use()
        mesh.draw()