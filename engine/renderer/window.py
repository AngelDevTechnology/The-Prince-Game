import glfw


class Window:
    def __init__(self, title: str = "The Prince", toggle_cursor_key: int = 258) -> None:
        if not glfw.init():
            raise RuntimeError("Impossible d'initialiser GLFW")

        monitor = self._choose_monitor()
        video_mode = glfw.get_video_mode(monitor)

        if video_mode is None:
            glfw.terminate()
            raise RuntimeError("Impossible de récupérer le mode vidéo")

        self.width = video_mode.size.width
        self.height = video_mode.size.height

        self.handle = glfw.create_window(self.width, self.height, title, monitor, None)
        if self.handle is None:
            glfw.terminate()
            raise RuntimeError("Impossible de créer la fenêtre")

        glfw.make_context_current(self.handle)
        glfw.swap_interval(1)

        # camera mode
        glfw.set_input_mode(self.handle, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.toggle_cursor_key = toggle_cursor_key
        self.cursor_captured = True
        self._toggle_key_was_pressed = False
        self.camera = None

    @staticmethod
    def _choose_monitor():
        """choose between monitors"""
        monitors = glfw.get_monitors()

        if not monitors:
            raise RuntimeError("Aucun moniteur détecté")

        for i, monitor in enumerate(monitors):
            print(i, glfw.get_monitor_name(monitor))

        choice = int(input("Moniteur : "))

        if not 0 <= choice < len(monitors):
            raise ValueError("Indice de moniteur invalide")

        return monitors[choice]

    def set_camera(self, camera) -> None:
        """set camera"""
        self.camera = camera
    
        self.camera.cursor_captured = self.cursor_captured
        self.camera.first_mouse = True

    def change_cursor_mode(self) -> None:
        """change cursor mode"""
        self.cursor_captured = not self.cursor_captured
        mode = (glfw.CURSOR_DISABLED if self.cursor_captured else glfw.CURSOR_NORMAL)

        glfw.set_input_mode(self.handle, glfw.CURSOR, mode)

        if self.camera is not None:
            self.camera.cursor_captured = self.cursor_captured
            self.camera.first_mouse = True

    def get_cursor_position(self):
        """return cursor position"""
        return glfw.get_cursor_pos(self.handle)
    
    def get_mouse_button(self, button):
        """get the mouse button"""
        return glfw.get_mouse_button(self.handle, button)
    
    def get_key_state(self, key):
        """get the key"""
        return glfw.get_key(self.handle, key)

    def handle_camera_mouse(self, glfw_window, xpos, ypos) -> None:
        if self.cursor_captured and self.camera is not None:
            self.camera.handle_mouse(glfw_window, xpos, ypos)

    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self.handle))

    def update(self):
        glfw.poll_events()
    
        pressed = glfw.get_key(
            self.handle,
            self.toggle_cursor_key
        ) == glfw.PRESS
    
        if pressed and not self._toggle_key_was_pressed:
            self.change_cursor_mode()
    
        self._toggle_key_was_pressed = pressed
    
        if (
            glfw.get_key(self.handle, glfw.KEY_ESCAPE) == glfw.PRESS
            and glfw.get_key(self.handle, glfw.KEY_LEFT_CONTROL) == glfw.PRESS
        ):
            glfw.set_window_should_close(self.handle, True)
    
    
    def swap_buffers(self):
        glfw.swap_buffers(self.handle)

    def destroy(self) -> None:
        """destroy it all"""
        glfw.destroy_window(self.handle)
        glfw.terminate()
