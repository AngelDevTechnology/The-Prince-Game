from imgui_bundle import imgui
from imgui_bundle.python_backends.glfw_backend import GlfwRenderer
from OpenGL.GL import GL_VERSION, glGetString
import glfw

from engine.database.database import Database
from engine.renderer.ui_content import GameUI
from engine.renderer.window import Window


class ImGuiManager:
    """Manage ImGui initialization, input, rendering, and shutdown."""

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, window: Window, database: Database) -> None:
        """Initialize ImGui only after activating a valid GL context."""

        self.window = window
        self.impl = None
        self._context_created = False
        self._callbacks_registered = False
        self._closed = False

        # --------------------------------------------------------
        # Activate and verify the OpenGL context
        # --------------------------------------------------------

        self.window.make_context_current()

        gl_version = glGetString(GL_VERSION)

        if gl_version is None:
            raise RuntimeError(
                "OpenGL ne voit aucun contexte courant. "
                "Vérifiez la création de la fenêtre GLFW."
            )

        # --------------------------------------------------------
        # Initialize ImGui context and GLFW/OpenGL backend
        # --------------------------------------------------------

        try:
            imgui.create_context()
            self._context_created = True

            self.impl = GlfwRenderer(
                self.window.handle,
                attach_callbacks=False,
            )

            # ----------------------------------------------------
            # Initialize UI content
            # ----------------------------------------------------

            self.ui = GameUI(database)
            self._was_cursor_captured = self.window.cursor_captured

            # ----------------------------------------------------
            # Register GLFW callbacks
            # ----------------------------------------------------

            glfw.set_key_callback(
                self.window.handle,
                self.impl.keyboard_callback,
            )

            glfw.set_cursor_pos_callback(
                self.window.handle,
                self._cursor_pos_callback,
            )

            glfw.set_mouse_button_callback(
                self.window.handle,
                self._mouse_button_callback,
            )

            glfw.set_window_size_callback(
                self.window.handle,
                self.impl.resize_callback,
            )

            glfw.set_char_callback(
                self.window.handle,
                self.impl.char_callback,
            )

            glfw.set_scroll_callback(
                self.window.handle,
                self._scroll_callback,
            )

            self._callbacks_registered = True

        except Exception:
            self._cleanup_initialization()
            raise

    # ============================================================
    # INITIALIZATION CLEANUP
    # ============================================================

    def _cleanup_initialization(self) -> None:
        """Release partially initialized ImGui resources."""

        try:
            if self.window.handle is not None:
                self.window.make_context_current()

            if self._callbacks_registered:
                self._unregister_callbacks()

            if self.impl is not None:
                self.impl.shutdown()
                self.impl = None

        finally:
            if self._context_created:
                imgui.destroy_context()
                self._context_created = False

    # ============================================================
    # GLFW CALLBACK MANAGEMENT
    # ============================================================

    def _unregister_callbacks(self) -> None:
        """Remove callbacks registered by this manager."""

        handle = self.window.handle

        if handle is None:
            return

        glfw.set_key_callback(handle, None)
        glfw.set_cursor_pos_callback(handle, None)
        glfw.set_mouse_button_callback(handle, None)
        glfw.set_window_size_callback(handle, None)
        glfw.set_char_callback(handle, None)
        glfw.set_scroll_callback(handle, None)

        self._callbacks_registered = False

    # ============================================================
    # INPUT HANDLING
    # ============================================================

    def _cursor_pos_callback(
        self,
        glfw_window,
        xpos: float,
        ypos: float,
    ) -> None:
        """Route cursor movement to the camera or ImGui."""

        if self.window.cursor_captured:
            imgui.get_io().add_mouse_pos_event(-1.0, -1.0)

            self.window.handle_camera_mouse(
                glfw_window,
                xpos,
                ypos,
            )
            return

        self.impl.mouse_callback(
            glfw_window,
            xpos,
            ypos,
        )

    def _mouse_button_callback(
        self,
        glfw_window,
        button: int,
        action: int,
        mods: int,
    ) -> None:
        """Forward mouse clicks to ImGui when the cursor is visible."""

        if not self.window.cursor_captured:
            self.impl.mouse_button_callback(
                glfw_window,
                button,
                action,
                mods,
            )

    def _scroll_callback(
        self,
        glfw_window,
        xoffset: float,
        yoffset: float,
    ) -> None:
        """Forward scrolling to ImGui when the cursor is visible."""

        if not self.window.cursor_captured:
            self.impl.scroll_callback(
                glfw_window,
                xoffset,
                yoffset,
            )

    # ============================================================
    # RENDERING
    # ============================================================

    def render(self) -> None:
        """Process input, build the UI frame, and render it."""

        if self._closed or self.impl is None:
            raise RuntimeError("ImGuiManager is already closed.")

        # The context may have been switched by another subsystem.
        self.window.make_context_current()

        self.impl.process_inputs()

        io = imgui.get_io()

        # --------------------------------------------------------
        # Synchronize cursor state
        # --------------------------------------------------------

        if self.window.cursor_captured:
            io.add_mouse_pos_event(-1.0, -1.0)

            if not self._was_cursor_captured:
                for button in range(5):
                    io.add_mouse_button_event(button, False)

        self._was_cursor_captured = self.window.cursor_captured

        # --------------------------------------------------------
        # Build and render ImGui frame
        # --------------------------------------------------------

        imgui.new_frame()

        if not self.window.cursor_captured:
            self.ui.render()

        imgui.render()
        self.impl.render(imgui.get_draw_data())

    # ============================================================
    # SHUTDOWN
    # ============================================================

    def shutdown(self) -> None:
        """Release backend resources while the OpenGL context is valid."""

        if self._closed:
            return

        self.window.make_context_current()

        try:
            if self._callbacks_registered:
                self._unregister_callbacks()

            if self.impl is not None:
                self.impl.shutdown()
                self.impl = None

        finally:
            if self._context_created:
                imgui.destroy_context()
                self._context_created = False

            self._closed = True
