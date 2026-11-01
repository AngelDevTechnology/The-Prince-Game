from imgui_bundle import imgui
import glfw

from imgui_bundle.python_backends.glfw_backend import GlfwRenderer

from engine.database.database import Database
from engine.renderer.ui_content import GameUI
from engine.renderer.window import Window


class ImGuiManager:
    """Manage ImGui initialization, input handling, rendering, and shutdown."""

    def __init__(self, window: Window, database: Database) -> None:
        """Initialize the ImGui context, GLFW backend, UI, and callbacks."""

        self.window = window

        # Initialize ImGui context.
        imgui.create_context()

        # Initialize GLFW backend.
        self.impl = GlfwRenderer(
            window.handle,
            attach_callbacks=False,
        )

        # Initialize UI content.
        self.ui = GameUI(database)

        self._was_cursor_captured = window.cursor_captured

        # Register GLFW callbacks.
        glfw.set_key_callback(
            window.handle,
            self.impl.keyboard_callback,
        )

        glfw.set_cursor_pos_callback(
            window.handle,
            self._cursor_pos_callback,
        )

        glfw.set_mouse_button_callback(
            window.handle,
            self._mouse_button_callback,
        )

        glfw.set_window_size_callback(
            window.handle,
            self.impl.resize_callback,
        )

        glfw.set_char_callback(
            window.handle,
            self.impl.char_callback,
        )

        glfw.set_scroll_callback(
            window.handle,
            self._scroll_callback,
        )

    # ==================================================
    # INPUT HANDLING
    # ==================================================

    def _cursor_pos_callback(self, glfw_window, xpos, ypos):
        """Handle cursor movement depending on the cursor capture state."""

        if self.window.cursor_captured:
            # Forward mouse movement to the camera.
            imgui.get_io().add_mouse_pos_event(-1.0, -1.0)

            self.window.handle_camera_mouse(
                glfw_window,
                xpos,
                ypos,
            )

            return

        # Forward mouse movement to ImGui.
        self.impl.mouse_callback(
            glfw_window,
            xpos,
            ypos,
        )

    def _mouse_button_callback(self, glfw_window, button, action, mods):
        """Forward mouse button events to ImGui when the cursor is free."""

        if not self.window.cursor_captured:
            self.impl.mouse_button_callback(
                glfw_window,
                button,
                action,
                mods,
            )

    def _scroll_callback(self, glfw_window, xoffset, yoffset):
        """Forward scroll events to ImGui when the cursor is free."""

        if not self.window.cursor_captured:
            self.impl.scroll_callback(
                glfw_window,
                xoffset,
                yoffset,
            )

    # ==================================================
    # RENDERING
    # ==================================================

    def render(self) -> None:
        """Process inputs, update the UI, and render the ImGui frame."""

        # Process incoming inputs.
        self.impl.process_inputs()

        io = imgui.get_io()

        # Synchronize cursor state with ImGui.
        if self.window.cursor_captured:
            io.add_mouse_pos_event(-1.0, -1.0)

            # Release any potentially active mouse buttons.
            if not self._was_cursor_captured:
                for button in range(5):
                    io.add_mouse_button_event(
                        button,
                        False,
                    )

        self._was_cursor_captured = self.window.cursor_captured

        # Begin a new ImGui frame.
        imgui.new_frame()

        # Display UI only when the cursor is free.
        if not self.window.cursor_captured:
            self.ui.render()

        # Render ImGui draw data.
        imgui.render()

        self.impl.render(
            imgui.get_draw_data(),
        )

    # ==================================================
    # SHUTDOWN
    # ==================================================

    def shutdown(self) -> None:
        """Unregister GLFW callbacks and release ImGui resources."""

        handle = self.window.handle

        # Unregister GLFW callbacks.
        glfw.set_key_callback(handle, None)
        glfw.set_cursor_pos_callback(handle, None)
        glfw.set_mouse_button_callback(handle, None)
        glfw.set_window_size_callback(handle, None)
        glfw.set_char_callback(handle, None)
        glfw.set_scroll_callback(handle, None)

        # Release backend resources.
        self.impl.shutdown()

        # Destroy ImGui context.
        imgui.destroy_context()