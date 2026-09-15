import glfw


class Window:
    def __init__(self, title: str = "The Prince") -> None:
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



    @staticmethod
    def _choose_monitor():
        monitors = glfw.get_monitors()

        i = 0
        for monitor in monitors:
            print(i, glfw.get_monitor_name(monitor))
            i += 1  

        choice = int(input("Moniteur : "))
        return monitors[choice]



    def should_close(self) -> bool:
        return glfw.window_should_close(self.handle)



    def update(self) -> None:
        glfw.poll_events()

        if (glfw.get_key(self.handle, glfw.KEY_ESCAPE) == glfw.PRESS and glfw.get_key(self.handle, glfw.KEY_LEFT_CONTROL) == glfw.PRESS):
            glfw.set_window_should_close(self.handle, True)

        glfw.swap_buffers(self.handle)



    def destroy(self) -> None:
        glfw.destroy_window(self.handle)
        glfw.terminate()

