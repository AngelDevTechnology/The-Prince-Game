from engine.renderer.window import Window
from engine.renderer.shader import Shader
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer


def main() -> None:
    window = Window("The Prince")
    
    shader = Shader("engine/shaders/basic.vert", "engine/shaders/basic.frag")
    
    triangle = Mesh([
    # Triangle 1
    -0.8,  0.5, 0.0,
    -0.8, -0.5, 0.0,
    -0.2, -0.5, 0.0,

    # Triangle 2
     0.2,  0.5, 0.0,
     0.2, -0.5, 0.0,
     0.8, -0.5, 0.0,
])

    renderer = Renderer(shader)

    try:
        while not window.should_close():
            renderer.render(triangle)
            window.update()


    finally:
        triangle.destroy()
        shader.destroy()
        window.destroy()


if __name__ == "__main__":
    main()
