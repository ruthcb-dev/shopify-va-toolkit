import tkinter as tk
from tkinter import ttk


class LogPanel:
    """
    Displays application activity logs.
    """

    def __init__(self, parent):

        self.frame = ttk.Frame(parent)

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Activity Log",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(5, 5)
        )

        self.log = tk.Text(
            self.frame,
            height=8,
            wrap="word",
            state="disabled"
        )

        scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.log.yview
        )

        self.log.configure(
            yscrollcommand=scrollbar.set
        )

        self.log.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=(0, 10)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=(0, 10)
        )

    def write(self, message):

        self.log.configure(state="normal")

        self.log.insert(
            tk.END,
            message + "\n"
        )

        self.log.see(tk.END)

        self.log.configure(state="disabled")

    def clear(self):

        self.log.configure(state="normal")

        self.log.delete(
            "1.0",
            tk.END
        )

        self.log.configure(state="disabled")