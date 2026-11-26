from __future__ import annotations

from typing import Any

import glfw


class Window:
    """
    GLFW window manager.

    Handles:
        - GLFW and OpenGL context initialization.
        - Window creation and destruction.
        - Monitor selection.
        - Keyboard and mouse input.
        - Cursor capture.
        - Camera mouse input.
        - Event polling and buffer swapping.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        title: str = "The Prince",
        toggle_cursor_key: int = glfw.KEY_TAB,
    ) -> None:
        """Create the game window and activate its OpenGL context."""

        if not glfw.init():
            raise RuntimeError("Impossible d'initialiser GLFW")

        self.handle: Any = None
        self._destroyed = False
        self.camera = None

        try:
            self.monitor = self._choose_monitor()
            video_mode = glfw.get_video_mode(self.monitor)

            if video_mode is None:
                raise RuntimeError(
                    "Impossible de récupérer le mode vidéo"
                )

            self.width = video_mode.size.width
            self.height = video_mode.size.height

            # ----------------------------------------------------
            # OpenGL context configuration
            # ----------------------------------------------------

            glfw.default_window_hints()
            glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(
                glfw.OPENGL_PROFILE,
                glfw.OPENGL_CORE_PROFILE,
            )

            # ----------------------------------------------------
            # Window creation
            # ----------------------------------------------------

            self.handle = glfw.create_window(
                self.width,
                self.height,
                title,
                self.monitor,
                None,
            )

            if self.handle is None:
                raise RuntimeError(
                    "Impossible de créer la fenêtre OpenGL"
                )

            # A context must be current before any OpenGL call.
            self.make_context_current()

            glfw.swap_interval(1)

            # ----------------------------------------------------
            # Cursor configuration
            # ----------------------------------------------------

            self.toggle_cursor_key = toggle_cursor_key
            self.cursor_captured = True

            glfw.set_input_mode(
                self.handle,
                glfw.CURSOR,
                glfw.CURSOR_DISABLED,
            )

            # ----------------------------------------------------
            # Input state
            # ----------------------------------------------------

            self._toggle_key_was_pressed = False
            self._close_key_was_pressed = False

        except Exception:
            if self.handle is not None:
                glfw.destroy_window(self.handle)
                self.handle = None

            glfw.terminate()
            self._destroyed = True
            raise

    # ============================================================
    # OPENGL CONTEXT
    # ============================================================

    def make_context_current(self) -> None:
        """Activate this window's OpenGL context on the current thread."""

        if self.handle is None or self._destroyed:
            raise RuntimeError(
                "Cannot activate an OpenGL context for a destroyed window."
            )

        glfw.make_context_current(self.handle)

        if not glfw.get_current_context():
            raise RuntimeError(
                "GLFW n'a pas réussi à activer le contexte OpenGL."
            )

    # ============================================================
    # MONITOR
    # ============================================================

    @staticmethod
    def _choose_monitor():
        """Ask the user to select an available monitor."""

        monitors = glfw.get_monitors()

        if not monitors:
            raise RuntimeError("Aucun moniteur détecté")

        for index, monitor in enumerate(monitors):
            print(
                f"{index}: {glfw.get_monitor_name(monitor)}"
            )

        while True:
            try:
                choice = int(input("Moniteur : "))

            except ValueError:
                print("Veuillez entrer un nombre valide.")
                continue

            except EOFError as exc:
                raise RuntimeError(
                    "Impossible de lire le moniteur sélectionné"
                ) from exc

            if 0 <= choice < len(monitors):
                return monitors[choice]

            print(
                f"Choisissez un indice entre 0 et {len(monitors) - 1}."
            )

    # ============================================================
    # CAMERA
    # ============================================================

    def set_camera(self, camera: Any) -> None:
        """Attach the camera to the window input manager."""

        self.camera = camera
        self.camera.cursor_captured = self.cursor_captured
        self.camera.first_mouse = True

    def handle_camera_mouse(
        self,
        glfw_window: Any,
        xpos: float,
        ypos: float,
    ) -> None:
        """Forward cursor movement to the camera when captured."""

        if self.camera is None or not self.cursor_captured:
            return

        self.camera.handle_mouse(
            glfw_window,
            xpos,
            ypos,
        )

    # ============================================================
    # CURSOR
    # ============================================================

    def change_cursor_mode(self) -> None:
        """Toggle between captured and visible cursor modes."""

        self.cursor_captured = not self.cursor_captured

        mode = (
            glfw.CURSOR_DISABLED
            if self.cursor_captured
            else glfw.CURSOR_NORMAL
        )

        glfw.set_input_mode(
            self.handle,
            glfw.CURSOR,
            mode,
        )

        if self.camera is not None:
            self.camera.cursor_captured = self.cursor_captured
            self.camera.first_mouse = True

    # ============================================================
    # INPUT
    # ============================================================

    def get_cursor_position(self):
        return glfw.get_cursor_pos(self.handle)

    def get_mouse_button(self, button: int) -> int:
        return glfw.get_mouse_button(self.handle, button)

    def get_key_state(self, key: int) -> int:
        return glfw.get_key(self.handle, key)

    def is_key_pressed(self, key: int) -> bool:
        return self.get_key_state(key) == glfw.PRESS

    def is_mouse_pressed(self, button: int) -> bool:
        return self.get_mouse_button(button) == glfw.PRESS

    # ============================================================
    # EVENTS
    # ============================================================

    def update(self) -> None:
        """Poll GLFW events and process local keyboard shortcuts."""

        glfw.poll_events()

        self._handle_cursor_toggle()
        self._handle_close_shortcut()

    def _handle_cursor_toggle(self) -> None:
        """Toggle cursor capture on a key-down transition."""

        pressed = self.is_key_pressed(self.toggle_cursor_key)

        if pressed and not self._toggle_key_was_pressed:
            self.change_cursor_mode()

        self._toggle_key_was_pressed = pressed

    def _handle_close_shortcut(self) -> None:
        """Close the window when Ctrl+Escape is pressed."""

        ctrl_pressed = (
            self.is_key_pressed(glfw.KEY_LEFT_CONTROL)
            or self.is_key_pressed(glfw.KEY_RIGHT_CONTROL)
        )

        escape_pressed = self.is_key_pressed(glfw.KEY_ESCAPE)
        pressed = ctrl_pressed and escape_pressed

        if pressed and not self._close_key_was_pressed:
            glfw.set_window_should_close(
                self.handle,
                True,
            )

        self._close_key_was_pressed = pressed

    # ============================================================
    # WINDOW STATE
    # ============================================================

    def should_close(self) -> bool:
        """Return whether the window should close."""

        return bool(glfw.window_should_close(self.handle))

    def swap_buffers(self) -> None:
        """Present the rendered frame."""

        glfw.swap_buffers(self.handle)

    # ============================================================
    # RESOURCE DESTRUCTION
    # ============================================================

    def destroy(self) -> None:
        """Destroy the window and terminate GLFW exactly once."""

        if self._destroyed:
            return

        if self.handle is not None:
            glfw.destroy_window(self.handle)
            self.handle = None

        glfw.terminate()
        self._destroyed = True
