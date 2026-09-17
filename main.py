from engine.renderer.window import Window
from engine.renderer.shader import Shader
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer

from OpenGL.GL import *


def main() -> None:
    window = Window("The Prince")
    
    shader = Shader("engine/shaders/basic.vert", "engine/shaders/basic.frag")
    
    while not window.should_close():
        glClear(GL_COLOR_BUFFER_BIT)

        shader.use()

        # Triangle

        window.update()

if __name__ == "__main__":
    main()
