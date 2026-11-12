import sqlite3

from imgui_bundle import imgui

from engine.renderer.ui_theme import MedievalTheme


class GameUI:

    def __init__(self, database) -> None:
        """Initialize the game UI and its state."""
        self.db = database

        MedievalTheme.apply()

        # ----------------------------------------------
        # NAVIGATION
        # ----------------------------------------------

        self.active_page = "Conseil"

        # ----------------------------------------------
        # DONNÉES
        # ----------------------------------------------

        self.characters = []
        self.plots = []
        self.kingdom = {}

        self.notification = (
            "Bienvenue dans le cabinet du Prince."
        )

        # ----------------------------------------------
        # PERSONNAGE SÉLECTIONNÉ
        # ----------------------------------------------

        self.selected_character_id = None
        self.selected_character = None

        self.edit_name = ""
        self.edit_role = ""
        self.edit_ambition = 20
        self.edit_loyalty = 70
        self.edit_is_player = False

        # ----------------------------------------------
        # CRÉATION PERSONNAGE
        # ----------------------------------------------

        self.new_name = ""
        self.new_role = "courtier"
        self.new_ambition = 20
        self.new_loyalty = 70

        # ----------------------------------------------
        # PLOTS
        # ----------------------------------------------

        self.plot_initiator_id = None
        self.plot_target_id = None

        # Chargement initial
        self.refresh_data()

    # ==================================================
    # COULEURS
    # ==================================================

    @staticmethod
    def gold():
        """Return the UI accent color."""
        return imgui.ImVec4(
            0.76, 0.60, 0.31, 1.0
        )

    @staticmethod
    def parchment():
        """Return the parchment text color."""
        return imgui.ImVec4(
            0.85, 0.79, 0.65, 1.0
        )

    @staticmethod
    def muted():
        """Return the muted text color."""
        return imgui.ImVec4(
            0.48, 0.44, 0.37, 1.0
        )

    # ==================================================
    # DONNÉES
    # ==================================================

    def refresh_data(self) -> None:
        """Reload game data and synchronize the current selections."""
        self.characters = self.db.get_all_characters()
        self.plots = self.db.get_all_plots()
        self.kingdom = self.db.get_kingdom()

        character_ids = {
            character["idPNJ"]
            for character in self.characters
        }

        # Conservation de la sélection
        selected = next(
            (
                character
                for character in self.characters
                if character["idPNJ"] == self.selected_character_id
            ),
            None
        )

        if selected is None:

            self.selected_character = None
            self.selected_character_id = None

            if self.characters:
                self.select_character(self.characters[0])

        else:
            self.select_character(selected)

        # Vérification de l'initiator
        if self.plot_initiator_id not in character_ids:

            self.plot_initiator_id = (
                self.characters[0]["idPNJ"]
                if self.characters else None
            )

        # Vérification de la target
        if (
            self.plot_target_id not in character_ids
            or self.plot_target_id == self.plot_initiator_id
        ):

            self.plot_target_id = next(
                (
                    character["idPNJ"]
                    for character in self.characters
                    if character["idPNJ"] != self.plot_initiator_id
                ),
                None
            )

    # ==================================================
    # NAVIGATION
    # ==================================================

    def nav_button(self, label: str, page: str) -> None:
        """Render a navigation button and update the active page when clicked."""
        selected = self.active_page == page

        if selected:

            imgui.push_style_color(
                imgui.Col_.button,
                imgui.ImVec4(0.48, 0.20, 0.19, 1.0)
            )

            imgui.push_style_color(
                imgui.Col_.button_hovered,
                imgui.ImVec4(0.58, 0.25, 0.22, 1.0)
            )

        if imgui.button(
            label,
            imgui.ImVec2(145, 38)
        ):
            self.active_page = page

        if selected:
            imgui.pop_style_color(2)

    # ==================================================
    # HEADER
    # ==================================================

    def render_header(self) -> None:
        """Render the application header and navigation controls."""
        imgui.text_colored(
            self.gold(),
            "THE PRINCE"
        )

        imgui.same_line()

        imgui.text_disabled(
            "// LE CABINET DU PRINCE"
        )

        imgui.spacing()

        imgui.text_colored(
            self.parchment(),
            "Le pouvoir ne se reçoit pas. Il se construit."
        )

        imgui.separator()

        self.nav_button("CONSEIL", "Conseil")
        imgui.same_line()

        self.nav_button("COUR", "Cour")
        imgui.same_line()

        self.nav_button("PLOTS", "Plots")
        imgui.same_line()

        self.nav_button("ROYAUME", "Royaume")

        imgui.separator()
        imgui.spacing()

    # ==================================================
    # CONSEIL
    # ==================================================

    def render_council(self) -> None:
        """Render the council overview and the latest plots."""
        active_plots = [
            plot for plot in self.plots
            if plot["successful"] is None
        ]

        imgui.text_colored(
            self.gold(),
            "I. ÉTAT DU CABINET"
        )

        imgui.spacing()

        imgui.text(
            f"Jour du royaume : {self.kingdom.get('jours', 1)}"
        )

        imgui.text(
            f"Personnages connus : {len(self.characters)}"
        )

        imgui.text(
            f"Plots actifs : {len(active_plots)}"
        )

        imgui.text(
            f"Plots enregistrés : {len(self.plots)}"
        )

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "II. DERNIÈRES INTRIGUES"
        )

        if not self.plots:

            imgui.text_disabled(
                "Aucune intrigue enregistrée."
            )

        for plot in self.plots[:5]:

            imgui.text(
                f"{plot['initiator_name']} "
                f"-> {plot['target_name']}"
            )

            if plot["successful"] is None:

                imgui.same_line()

                imgui.text_colored(
                    self.gold(),
                    "[EN COURS]"
                )

            elif plot["successful"]:

                imgui.same_line()

                imgui.text_colored(
                    imgui.ImVec4(0.35, 0.75, 0.40, 1.0),
                    "[RÉUSSI]"
                )

            else:

                imgui.same_line()

                imgui.text_disabled(
                    "[ÉCHOUÉ]"
                )

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "III. MESSAGE DU CONSEILLER"
        )

        imgui.text_wrapped(self.notification)

    # ==================================================
    # SÉLECTION PERSONNAGE
    # ==================================================

    def select_character(self, character) -> None:
        """Select a character and populate its editable fields."""
        self.selected_character = character
        self.selected_character_id = character["idPNJ"]

        self.edit_name = character["name"]
        self.edit_role = character["role"] or "peasant"

        self.edit_ambition = character["ambition"]
        self.edit_loyalty = character["loyalty"]

        self.edit_is_player = bool(
            character["is_player"]
        )

    # ==================================================
    # SAUVEGARDE PERSONNAGE
    # ==================================================

    def save_character(self) -> None:
        """Validate and save the currently selected character."""
        if self.selected_character is None:
            return

        character_id = self.selected_character_id

        values = {
            "name": self.edit_name.strip(),
            "role": self.edit_role.strip(),
            "ambition": self.edit_ambition,
            "loyalty": self.edit_loyalty,
            "is_player": int(self.edit_is_player),
        }

        if not values["name"]:
            self.notification = "Le nom ne peut pas être vide."
            return

        if not values["role"]:
            self.notification = "Le rôle ne peut pas être vide."
            return

        try:

            for column, value in values.items():

                old_value = self.selected_character[column]

                if value != old_value:

                    self.db.update(
                        value,
                        "PNJ",
                        column,
                        character_id,
                    )

            self.refresh_data()

            self.notification = (
                f"{self.edit_name} : modifications sauvegardées."
            )

        except (ValueError, sqlite3.Error) as error:

            self.notification = (
                f"Erreur de sauvegarde : {error}"
            )

    # ==================================================
    # COUR
    # ==================================================

    def render_characters(self) -> None:
        """Render the character registry, editor, and recruitment controls."""
        imgui.text_colored(
            self.gold(),
            "I. REGISTRE DE LA COUR"
        )

        imgui.spacing()

        if not self.characters:

            imgui.text_disabled(
                "Aucun personnage dans le royaume."
            )

        for character in self.characters:

            character_id = character["idPNJ"]

            selected = (
                character_id == self.selected_character_id
            )

            label = (
                f"{character['name']} "
                f"({character['role']})"
                f"##pnj_{character_id}"
            )

            clicked, _ = imgui.selectable(
                label,
                selected
            )

            if clicked:
                self.select_character(character)

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "II. FICHE DU PERSONNAGE"
        )

        if self.selected_character is not None:

            _, self.edit_name = imgui.input_text(
                "Nom",
                self.edit_name
            )

            _, self.edit_role = imgui.input_text(
                "Rôle",
                self.edit_role
            )

            _, self.edit_ambition = imgui.slider_int(
                "Ambition",
                self.edit_ambition,
                0,
                100
            )

            _, self.edit_loyalty = imgui.slider_int(
                "Loyauté",
                self.edit_loyalty,
                0,
                100
            )

            _, self.edit_is_player = imgui.checkbox(
                "Personnage du joueur",
                self.edit_is_player
            )

            if imgui.button(
                "SAUVEGARDER",
                imgui.ImVec2(180, 38)
            ):
                self.save_character()

        imgui.spacing()
        imgui.separator()

        # ----------------------------------------------
        # RECRUTEMENT
        # ----------------------------------------------

        imgui.text_colored(
            self.gold(),
            "III. RECRUTEMENT"
        )

        _, self.new_name = imgui.input_text(
            "Nom du nouveau personnage",
            self.new_name
        )

        _, self.new_role = imgui.input_text(
            "Rôle initial",
            self.new_role
        )

        _, self.new_ambition = imgui.slider_int(
            "Ambition initiale",
            self.new_ambition,
            0,
            100
        )

        _, self.new_loyalty = imgui.slider_int(
            "Loyauté initiale",
            self.new_loyalty,
            0,
            100
        )

        if imgui.button(
            "RECRUTER",
            imgui.ImVec2(180, 38)
        ):

            if not self.new_name.strip():

                self.notification = (
                    "Le nom du personnage est obligatoire."
                )

            elif not self.new_role.strip():

                self.notification = (
                    "Le rôle du personnage est obligatoire."
                )

            else:

                try:

                    new_id = self.db.add(
                        "PNJ",
                        {
                            "name": self.new_name.strip(),
                            "role": self.new_role.strip(),
                            "ambition": self.new_ambition,
                            "loyalty": self.new_loyalty,
                            "is_player": 0,
                        }
                    )

                    self.refresh_data()

                    new_character = next(
                        (
                            character
                            for character in self.characters
                            if character["idPNJ"] == new_id
                        ),
                        None
                    )

                    if new_character is not None:
                        self.select_character(new_character)

                    self.new_name = ""

                    self.notification = (
                        "Un nouveau personnage rejoint la cour."
                    )

                except (ValueError, sqlite3.Error) as error:

                    self.notification = (
                        f"Erreur de recrutement : {error}"
                    )

    # ==================================================
    # SÉLECTEUR DE PERSONNAGE
    # ==================================================

    def character_combo(
        self,
        label: str,
        selected_id: int | None,
        excluded_id: int | None = None,
    ) -> int | None:
        """Render a character selector and return the selected character ID."""
        selected_character = next(
            (
                character
                for character in self.characters
                if character["idPNJ"] == selected_id
            ),
            None
        )

        preview = (
            selected_character["name"]
            if selected_character
            else "Choisir un personnage..."
        )

        result = selected_id

        if imgui.begin_combo(label, preview):

            for character in self.characters:

                character_id = character["idPNJ"]

                if character_id == excluded_id:
                    continue

                is_selected = (
                    character_id == selected_id
                )

                clicked, _ = imgui.selectable(
                    f"{character['name']}##{label}_{character_id}",
                    is_selected
                )

                if clicked:
                    result = character_id

            imgui.end_combo()

        return result

    # ==================================================
    # PLOTS
    # ==================================================

    def render_plots(self) -> None:
        """Render plot creation controls and the plot registry."""
        imgui.text_colored(
            self.gold(),
            "I. NOUVEAU Plot"
        )

        imgui.spacing()

        if len(self.characters) < 2:

            imgui.text_disabled(
                "Il faut au moins deux personnages."
            )

        else:

            self.plot_initiator_id = self.character_combo(
                "initiator",
                self.plot_initiator_id
            )

            self.plot_target_id = self.character_combo(
                "target",
                self.plot_target_id,
                excluded_id=self.plot_initiator_id
            )

            if imgui.button(
                "ENREGISTRER LE Plot",
                imgui.ImVec2(230, 38)
            ):

                if (
                    self.plot_initiator_id is not None
                    and self.plot_target_id is not None
                    and self.plot_initiator_id != self.plot_target_id
                ):

                    try:

                        self.db.add(
                            "Plot",
                            {
                                "initiator_id": self.plot_initiator_id,
                                "target_id": self.plot_target_id,
                                "successful": None,
                            }
                        )

                        self.refresh_data()

                        self.notification = (
                            "Une nouvelle intrigue est enregistrée."
                        )

                    except sqlite3.Error as error:

                        self.notification = (
                            f"Erreur de création : {error}"
                        )

                else:

                    self.notification = (
                        "Sélectionne deux personnages différents."
                    )

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "II. REGISTRE DES PLOTS"
        )

        if not self.plots:

            imgui.text_disabled(
                "Aucun Plot enregistré."
            )

        for plot in self.plots:

            plot_id = plot["idplot"]

            imgui.separator()

            imgui.text(
                f"#{plot_id} : "
                f"{plot['initiator_name']} "
                f"-> {plot['target_name']}"
            )

            if plot["successful"] is None:

                imgui.text_colored(
                    self.gold(),
                    "Statut : EN COURS"
                )

                if imgui.button(
                    f"RÉUSSI##success_{plot_id}"
                ):

                    self.resolve_plot(plot_id, True)
                    return

                imgui.same_line()

                if imgui.button(
                    f"ÉCHOUÉ##failure_{plot_id}"
                ):

                    self.resolve_plot(plot_id, False)
                    return

            elif plot["successful"]:

                imgui.text_colored(
                    imgui.ImVec4(0.35, 0.75, 0.40, 1.0),
                    "Statut : RÉUSSI"
                )

            else:

                imgui.text_disabled(
                    "Statut : ÉCHOUÉ"
                )

    def resolve_plot(
        self,
        plot_id: int,
        success: bool
    ) -> None:
        """Update a plot with its final outcome."""
        try:

            self.db.update(
                int(success),
                "Plot",
                "successful",
                plot_id
            )

            self.refresh_data()

            self.notification = (
                "Le Plot a été marqué comme réussi."
                if success
                else "Le Plot a été marqué comme échoué."
            )

        except sqlite3.Error as error:

            self.notification = (
                f"Erreur de résolution : {error}"
            )

    # ==================================================
    # ROYAUME
    # ==================================================

    def render_kingdom(self) -> None:
        """Render kingdom statistics and the day advancement control."""
        day = self.kingdom.get("days", 1)

        imgui.text_colored(
            self.gold(),
            "I. CALENDRIER ROYAL"
        )

        imgui.spacing()

        imgui.text(
            f"Le royaume est actuellement au jour {day}."
        )

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "II. ÉTAT GÉNÉRAL"
        )

        imgui.text(
            f"Personnages : {len(self.characters)}"
        )

        imgui.text(
            f"Intrigues : {len(self.plots)}"
        )

        active_count = sum(
            plot["successful"] is None
            for plot in self.plots
        )

        imgui.text(
            f"Intrigues en cours : {active_count}"
        )

        imgui.spacing()
        imgui.separator()

        imgui.text_colored(
            self.gold(),
            "III. PASSAGE DU TEMPS"
        )

        if imgui.button(
            "PASSER AU JOUR SUIVANT",
            imgui.ImVec2(240, 42)
        ):

            try:

                self.db.advance_day()
                self.refresh_data()

                self.notification = (
                    f"Le royaume entre dans son jour {self.kingdom['days']}."
                )

            except sqlite3.Error as error:

                self.notification = (
                    f"Erreur : {error}"
                )

    # ==================================================
    # FOOTER
    # ==================================================

    def render_footer(self) -> None:
        """Render the application footer and current notification."""
        imgui.separator()

        imgui.text_disabled(
            "CONSEIL DU PRINCE"
        )

        imgui.text_wrapped(
            self.notification
        )

    # ==================================================
    # RENDU PRINCIPAL
    # ==================================================

    def render(self) -> None:
        """Render the main application window and its active page."""
        io = imgui.get_io()

        # ----------------------------------------------
        # POSITION ET DIMENSIONS
        # ----------------------------------------------

        imgui.set_next_window_pos(
            imgui.ImVec2(0.0, 0.0),
            imgui.Cond_.always
        )

        imgui.set_next_window_size(
            io.display_size,
            imgui.Cond_.always
        )

        # ----------------------------------------------
        # FENÊTRE FIXE
        # ----------------------------------------------

        flags = (
            imgui.WindowFlags_.no_title_bar
            | imgui.WindowFlags_.no_resize
            | imgui.WindowFlags_.no_move
            | imgui.WindowFlags_.no_collapse
            | imgui.WindowFlags_.no_saved_settings
        )

        imgui.begin(
            "The Prince | Cabinet royal",
            flags=flags
        )

        # ----------------------------------------------
        # HEADER
        # ----------------------------------------------

        self.render_header()

        # ----------------------------------------------
        # PAGE ACTIVE
        # ----------------------------------------------

        if self.active_page == "Conseil":

            self.render_council()

        elif self.active_page == "Cour":

            self.render_characters()

        elif self.active_page == "Plots":

            self.render_plots()

        elif self.active_page == "Royaume":

            self.render_kingdom()

        # ----------------------------------------------
        # FOOTER
        # ----------------------------------------------

        self.render_footer()

        imgui.end()
