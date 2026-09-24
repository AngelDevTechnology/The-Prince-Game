import time

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

    shader = Shader(
        "engine/shaders/basic.vert",
        "engine/shaders/basic.frag",
    )

    triangle = Mesh(vertices)

    start_time = time.perf_counter()

    try:
        shader.use()
        shader.set_vec3("color", (0.8, 0.2, 1.0))

        while not window.should_close():
            current_time = time.perf_counter() - start_time

            shader.set_float("time", current_time)

            renderer.clear()
            renderer.draw(shader, triangle)

            window.update()

    finally:
        triangle.destroy()
        shader.delete()
        window.destroy()


if __name__ == "__main__":
    main()