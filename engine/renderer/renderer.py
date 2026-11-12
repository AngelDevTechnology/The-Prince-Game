from __future__ import annotations

from OpenGL.GL import (
    GL_BACK,
    GL_CCW,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LESS,
    glClear,
    glClearColor,
    glCullFace,
    glDepthFunc,
    glEnable,
    glFrontFace,
)

from .mesh import Mesh
from .shader import Shader


class Renderer:
    """
    Gère l'état global du rendu OpenGL et les appels de dessin.

    Responsabilités :
        - Configurer les états OpenGL.
        - Effacer les buffers de rendu.
        - Activer les shaders.
        - Dessiner les maillages.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self) -> None:
        """Initialise le renderer et configure OpenGL."""

        self._configure_state()

    # ============================================================
    # RENDER STATE CONFIGURATION
    # ============================================================

    @staticmethod
    def _configure_state() -> None:
        """
        Configure les états OpenGL utilisés par le renderer.
        """

        # --------------------------------------------------------
        # Depth Testing
        # --------------------------------------------------------

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # --------------------------------------------------------
        # Back-Face Culling
        # --------------------------------------------------------

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

        # --------------------------------------------------------
        # Clear Color
        # --------------------------------------------------------

        glClearColor(0.05, 0.05, 0.07, 1.0)

    # ============================================================
    # FRAME BUFFER CLEARING
    # ============================================================

    @staticmethod
    def clear() -> None:
        """
        Efface les buffers de couleur et de profondeur.

        À appeler au début de chaque frame.
        """

        glClear(
            int(GL_COLOR_BUFFER_BIT)
            | int(GL_DEPTH_BUFFER_BIT)
        )

    # ============================================================
    # DRAW CALLS
    # ============================================================

    @staticmethod
    def draw(shader: Shader, mesh: Mesh) -> None:
        """
        Dessine un maillage avec un programme shader.

        Args:
            shader: Programme shader à utiliser.
            mesh: Maillage à dessiner.
        """

        # --------------------------------------------------------
        # Activate Shader
        # --------------------------------------------------------

        shader.use()

        # --------------------------------------------------------
        # Draw Mesh
        # --------------------------------------------------------

        mesh.draw()
