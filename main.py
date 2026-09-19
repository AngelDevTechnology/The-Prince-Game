from engine.renderer.window import Window
from engine.renderer.shader import Shader
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer


vertices = [
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0,
]


def main() -> None:
    window = Window("The Prince")
    renderer = Renderer()

    shader = Shader("engine/shaders/basic.vert", "engine/shaders/basic.frag")

    triangle = Mesh(vertices)

    try:
        while not window.should_close():

            renderer.clear()
            renderer.draw(shader, triangle)

            window.update()

    finally:
        triangle.destroy()
        window.destroy()
        shader.destroy()


if __name__ == "__main__":
    main()