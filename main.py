import time
import math

from engine.renderer.window import Window
from engine.renderer.shader import Shader
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer
from engine.math3d.mat4D import Mat4
from engine.math3d.vector3D import Vec3


vertices = [
    -0.5, -0.5, -0.5,  # 0
     0.5, -0.5, -0.5,  # 1
     0.5,  0.5, -0.5,  # 2
    -0.5,  0.5, -0.5,  # 3

    -0.5, -0.5,  0.5,  # 4
     0.5, -0.5,  0.5,  # 5
     0.5,  0.5,  0.5,  # 6
    -0.5,  0.5,  0.5,  # 7
]

indices = [
    # Avant
    4, 5, 6,
    4, 6, 7,

    # Arrière
    1, 0, 3,
    1, 3, 2,

    # Gauche
    0, 4, 7,
    0, 7, 3,

    # Droite
    5, 1, 2,
    5, 2, 6,

    # Dessus
    3, 7, 6,
    3, 6, 2,

    # Dessous
    0, 1, 5,
    0, 5, 4,
]


def main() -> None:
    window = Window("The Prince")
    renderer = Renderer()

    shader = Shader(
        "engine/shaders/basic.vert",
        "engine/shaders/basic.frag",
    )

    cube = Mesh(vertices, indices)

    try:
        shader.use()

        shader.set_vec3("color", (0.8, 0.2, 1.0))


        projection = Mat4.perspective(
            math.radians(70.0),
            window.width / window.height,
            0.1,
            100.0,
        )

        start_time = time.perf_counter()


        while not window.should_close():
            current_time = time.perf_counter() - start_time

            model = (
                Mat4.translation(Vec3(math.sin(current_time) * 0.5, math.cos(current_time) * 0.5, -2.0))
                @ Mat4.rotation_y(current_time)
                @ Mat4.rotation_z(current_time * 0.5)
            )

            mvp = projection @ model

            shader.use()
            shader.set_mat4("mvp", mvp)
            shader.set_float("time", current_time)

            renderer.clear()
            renderer.draw(shader, cube)
            window.update()

    finally:
        cube.destroy()
        shader.delete()
        window.destroy()


if __name__ == "__main__":
    main()
