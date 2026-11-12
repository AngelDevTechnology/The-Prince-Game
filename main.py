
# ============================================================
# LINUX / WAYLAND OPENGL CONFIGURATION
# ============================================================

import os
import sys

if (
    sys.platform.startswith("linux")
    and os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
):
    os.environ.setdefault("PYOPENGL_PLATFORM", "x11")


# ============================================================
# NATIVE LIBRARY INITIALIZATION
# ============================================================

# IMPORTANT:
# imgui_bundle must be imported before GLFW.

# isort: off
import imgui_bundle  # noqa: E402, F401
# isort: on


# ============================================================
# PROJECT IMPORTS
# ============================================================

import math
import time

from engine.database.database import Database
from engine.math3d.mat4d import Mat4
from engine.math3d.vector3d import Vec3
from engine.renderer.camera import Camera
from engine.renderer.loader import load_mesh_data
from engine.renderer.mesh import Mesh
from engine.renderer.renderer import Renderer
from engine.renderer.shader import Shader
from engine.renderer.ui import ImGuiManager
from engine.renderer.window import Window



# ============================================================
# GAME
# ============================================================

class Game:
    """Manage game initialization, updates, rendering, and shutdown."""

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self) -> None:
        """Initialize resources in an order that guarantees a GL context."""

        # Initialize references first so partial initialization can be cleaned.
        self.window = None
        self.database = None
        self.camera = None
        self.renderer = None
        self.imgui_manager = None
        self.shader = None
        self.mesh = None

        self.projection = None
        self.start_time = 0.0
        self._shutdown = False

        try:
            # ----------------------------------------------------
            # Window and OpenGL context
            # ----------------------------------------------------

            self.window = Window("The Prince")
            self.window.make_context_current()

            # ----------------------------------------------------
            # Database
            # ----------------------------------------------------

            self.database = Database()

            # ----------------------------------------------------
            # Camera
            # ----------------------------------------------------

            self.camera = Camera()
            self.window.set_camera(self.camera)

            # ----------------------------------------------------
            # ImGui backend
            # ----------------------------------------------------

            self.imgui_manager = ImGuiManager(
                self.window,
                self.database,
            )

            # ----------------------------------------------------
            # OpenGL renderer state
            # ----------------------------------------------------

            self.renderer = Renderer()

            # ----------------------------------------------------
            # Shader and mesh resources
            # ----------------------------------------------------

            self.shader = Shader(
                "engine/shaders/basic.vert",
                "engine/shaders/basic.frag",
            )

            positions, indices = load_mesh_data("911_scene.obj")
            self.mesh = Mesh(positions, indices)

            # ----------------------------------------------------
            # Projection and timing
            # ----------------------------------------------------

            if self.window.height <= 0:
                raise RuntimeError("Invalid window height.")

            self.projection = self.camera.get_projection_matrix(
                self.window.width / self.window.height,
            )

            self.start_time = time.perf_counter()

            # ----------------------------------------------------
            # Shader configuration
            # ----------------------------------------------------

            self._configure_shader()

        except Exception:
            self.shutdown()
            raise

    # ========================================================
    # SHADER CONFIGURATION
    # ========================================================

    def _configure_shader(self) -> None:
        """Configure shader uniforms and lighting properties."""

        self.shader.use()

        self.shader.set_vec3(
            "color",
            (0.8, 0.2, 1.0),
        )

        self.shader.set_vec3(
            "viewPos",
            (0.0, 0.0, 0.0),
        )

        lights = [
            ((2.0, 2.0, 1.0), (1.0, 1.0, 1.0)),
            ((-2.0, 1.0, 0.0), (1.0, 0.15, 0.1)),
            ((0.0, -1.5, 1.5), (0.1, 0.3, 1.0)),
        ]

        self.shader.set_int(
            "lightCount",
            len(lights),
        )

        for index, (position, color) in enumerate(lights):
            self.shader.set_vec3(
                f"lightPositions[{index}]",
                position,
            )

            self.shader.set_vec3(
                f"lightColors[{index}]",
                color,
            )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self) -> None:
        """Update the game state and process window events."""

        self.window.update()

    def _get_model_matrix(self) -> Mat4:
        """Calculate the animated model transformation."""

        current_time = time.perf_counter() - self.start_time

        translation = Mat4.translation(
            Vec3(
                math.sin(current_time) * 0.5,
                math.cos(current_time) * 0.5,
                -2.0,
            )
        )

        rotation_y = Mat4.rotation_y(current_time)
        rotation_z = Mat4.rotation_z(current_time * 0.5)

        return translation @ rotation_y @ rotation_z

    # ========================================================
    # RENDERING
    # ========================================================

    def render(self) -> None:
        """Render the 3D scene and the user interface."""

        self.window.make_context_current()

        self.renderer.clear()

        self.shader.use()

        self.shader.set_mat4(
            "model",
            self._get_model_matrix(),
        )

        self.shader.set_mat4(
            "view",
            self.camera.get_view_matrix(),
        )

        self.shader.set_mat4(
            "projection",
            self.projection,
        )

        self.renderer.draw(
            self.shader,
            self.mesh,
        )

        self.imgui_manager.render()
        self.window.swap_buffers()

    # ========================================================
    # GAME LOOP
    # ========================================================

    def run(self) -> None:
        """Execute the main game loop."""

        while not self.window.should_close():
            self.update()
            self.render()

    # ========================================================
    # SHUTDOWN
    # ========================================================

    def shutdown(self) -> None:
        """Release resources before destroying the OpenGL context."""

        if self._shutdown:
            return

        # Make the owning context current before deleting GL resources.
        if self.window is not None and self.window.handle is not None:
            self.window.make_context_current()

        # ImGui backend owns OpenGL resources and must be stopped
        # before the GLFW window/context is destroyed.
        if self.imgui_manager is not None:
            self.imgui_manager.shutdown()
            self.imgui_manager = None

        if self.mesh is not None:
            self.mesh.destroy()
            self.mesh = None

        if self.shader is not None:
            self.shader.delete()
            self.shader = None

        if self.database is not None:
            self.database.close()
            self.database = None

        if self.window is not None:
            self.window.destroy()
            self.window = None

        self._shutdown = True


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main() -> None:
    """Create, run, and shut down the game."""

    game = None

    try:
        game = Game()
        game.run()

    finally:
        if game is not None:
            game.shutdown()


if __name__ == "__main__":
    main()
