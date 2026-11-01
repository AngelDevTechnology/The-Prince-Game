from imgui_bundle import imgui


class MedievalTheme:
    """Define and apply the medieval visual theme for ImGui."""

    @staticmethod
    def apply() -> None:
        """Apply the dark theme, configure UI dimensions, and set the color palette."""

        imgui.style_colors_dark()

        style = imgui.get_style()

        # ==================================================
        # DIMENSIONS
        # ==================================================

        style.window_padding = imgui.ImVec2(16.0, 16.0)
        style.frame_padding = imgui.ImVec2(10.0, 7.0)
        style.item_spacing = imgui.ImVec2(10.0, 10.0)

        style.window_rounding = 5.0
        style.frame_rounding = 3.0
        style.popup_rounding = 4.0
        style.scrollbar_rounding = 4.0
        style.grab_rounding = 3.0

        style.window_border_size = 1.0
        style.frame_border_size = 1.0

        # ==================================================
        # COLOR PALETTE
        # ==================================================

        colors = {
            # Text.
            imgui.Col_.text: (0.85, 0.79, 0.65, 1.00),
            imgui.Col_.text_disabled: (0.48, 0.44, 0.37, 1.00),

            # Windows.
            imgui.Col_.window_bg: (0.09, 0.09, 0.08, 1.00),
            imgui.Col_.child_bg: (0.12, 0.11, 0.09, 1.00),
            imgui.Col_.popup_bg: (0.10, 0.09, 0.08, 1.00),

            # Borders.
            imgui.Col_.border: (0.40, 0.32, 0.20, 0.80),

            # Input fields.
            imgui.Col_.frame_bg: (0.16, 0.14, 0.11, 1.00),
            imgui.Col_.frame_bg_hovered: (0.30, 0.19, 0.16, 1.00),
            imgui.Col_.frame_bg_active: (0.38, 0.20, 0.19, 1.00),

            # Title bars.
            imgui.Col_.title_bg: (0.12, 0.10, 0.08, 1.00),
            imgui.Col_.title_bg_active: (0.25, 0.12, 0.13, 1.00),

            # Buttons.
            imgui.Col_.button: (0.32, 0.13, 0.16, 1.00),
            imgui.Col_.button_hovered: (0.48, 0.20, 0.19, 1.00),
            imgui.Col_.button_active: (0.60, 0.35, 0.20, 1.00),

            # Selection headers.
            imgui.Col_.header: (0.30, 0.15, 0.14, 1.00),
            imgui.Col_.header_hovered: (0.44, 0.19, 0.18, 1.00),
            imgui.Col_.header_active: (0.53, 0.24, 0.19, 1.00),

            # Checkmarks and sliders.
            imgui.Col_.check_mark: (0.76, 0.60, 0.31, 1.00),
            imgui.Col_.slider_grab: (0.68, 0.48, 0.23, 1.00),
            imgui.Col_.slider_grab_active: (0.83, 0.65, 0.36, 1.00),

            # Separators.
            imgui.Col_.separator: (0.38, 0.30, 0.19, 0.70),
            imgui.Col_.separator_hovered: (0.68, 0.48, 0.23, 1.00),
            imgui.Col_.separator_active: (0.83, 0.65, 0.36, 1.00),
        }

        # Apply the configured color palette.
        for color_id, color in colors.items():
            style.set_color_(color_id, color)