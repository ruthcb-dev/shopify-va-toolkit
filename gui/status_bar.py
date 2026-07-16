from tkinter import ttk


class StatusBar:
    """
    Displays the current application status.
    """

    def __init__(self, parent):

        self.frame = ttk.Frame(parent)

        self.frame.pack(fill="x")

        self.status = ttk.Label(
            self.frame,
            text="Ready",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            padx=10,
            pady=3
        )

    def set_status(self, message):

        self.status.config(text=message)