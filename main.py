import math
import time

from engine.math3d.mat4d import Mat4
from engine.math3d.vector3d import Vec3
from engine.renderer.camera import Camera
from engine.renderer.loader import load_mesh_data
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer
from engine.renderer.shader import Shader
from engine.renderer.window import Window

positions, indices = load_mesh_data("911_scene.obj")


def main() -> None:
    window = Window("The Prince")
    camera = Camera()
    window.set_camera(camera)

    renderer = Renderer()

    shader = Shader(
        "engine/shaders/basic.vert",
        "engine/shaders/basic.frag",
    )

    mesh = Mesh(positions, indices)

    try:
        shader.use()

        shader.set_vec3("color", (0.8, 0.2, 1.0))
        shader.set_vec3("viewPos", (0.0, 0.0, 0.0))

        lights = [
            # Position           Color
            ((2.0, 2.0, 1.0), (1.0, 1.0, 1.0)),  # White
            ((-2.0, 1.0, 0.0), (1.0, 0.15, 0.1)),  # Red
            ((0.0, -1.5, 1.5), (0.1, 0.3, 1.0)),  # Blue
        ]

        shader.set_int("lightCount", len(lights))

        for i, (position, light_color) in enumerate(lights):
            shader.set_vec3(f"lightPositions[{i}]", position)
            shader.set_vec3(f"lightColors[{i}]", light_color)

        projection = camera.get_projection_matrix(window.width / window.height)

        start_time = time.perf_counter()

        while not window.should_close():
            current_time = time.perf_counter() - start_time

            model = (
                Mat4.translation(
                    Vec3(
                        math.sin(current_time) * 0.5, math.cos(current_time) * 0.5, -2.0
                    )
                )
                @ Mat4.rotation_y(current_time)
                @ Mat4.rotation_z(current_time * 0.5)
            )

            view = camera.get_view_matrix()

            shader.use()

            shader.set_mat4("model", model)
            shader.set_mat4("view", view)
            shader.set_mat4("projection", projection)

            renderer.clear()
            renderer.draw(shader, mesh)
            window.update()

    finally:
        mesh.destroy()
        shader.delete()
        window.destroy()


if __name__ == "__main__":
    main()
