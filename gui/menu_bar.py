import tkinter as tk


class MenuBar:
    """
    Application menu bar.
    """

    def __init__(
        self,
        root,
        on_fetch=None,
        on_download=None,
        on_generate_csv=None,
        on_validate=None,
        on_export=None,
        on_settings=None,
        on_about=None,
        on_exit=None
    ):

        self.root = root
        self.on_exit = on_exit or self.root.destroy

        self.menu = tk.Menu(self.root)

        self.root.config(menu=self.menu)

        self.create_file_menu(
            on_fetch=on_fetch,
            on_generate_csv=on_generate_csv,
            on_export=on_export,
            on_settings=on_settings
        )

        self.create_tools_menu(
            on_download=on_download,
            on_validate=on_validate
        )

        self.create_help_menu(
            on_about=on_about
        )

    # ==========================================================
    # File Menu
    # ==========================================================

    def create_file_menu(
        self,
        on_fetch,
        on_generate_csv,
        on_export,
        on_settings
    ):

        file_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        file_menu.add_command(
            label="Fetch Products",
            command=on_fetch
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Generate CSV",
            command=on_generate_csv
        )

        file_menu.add_command(
            label="Export Selected",
            command=on_export
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Settings",
            command=on_settings
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.on_exit
        )

        self.menu.add_cascade(
            label="File",
            menu=file_menu
        )

    # ==========================================================
    # Tools Menu
    # ==========================================================

    def create_tools_menu(
        self,
        on_download,
        on_validate
    ):

        tools_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        tools_menu.add_command(
            label="Download Images",
            command=on_download
        )

        tools_menu.add_command(
            label="Validate CSV",
            command=on_validate
        )

        self.menu.add_cascade(
            label="Tools",
            menu=tools_menu
        )

    # ==========================================================
    # Help Menu
    # ==========================================================

    def create_help_menu(
        self,
        on_about
    ):

        help_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        help_menu.add_command(
            label="About",
            command=on_about
        )

        self.menu.add_cascade(
            label="Help",
            menu=help_menu
        )