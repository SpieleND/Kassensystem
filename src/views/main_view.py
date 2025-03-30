from tkinter import Tk, Frame

import os
from views.components.admin_menu import AdminMenu
from views.components.role_display import RoleDisplay

class MainView:
    def __init__(self, session):
        self.session = session
        self.root = Tk()
        self.root.title("Komponentenbasierte View")
        self.root.geometry(os.getenv("DISPLAY_RESOLUTION"))

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.role_display = RoleDisplay(self.main_frame, session)

        self.admin_menu = None

        self.root.bind("<l>", self.enter_admin_mode)

    def enter_admin_mode(self, event=None):
        """Wechselt in den administrativen Bereich."""
        self.clear_main_frame()

        # Admin-Menü anzeigen
        self.admin_menu = AdminMenu(self.main_frame, self.session, self.logout)

    def logout(self):
        """Wechselt zurück in den Standardmodus."""
        self.session.set_user(None)

        # Admin-Menü entfernen und Standardansicht anzeigen
        self.clear_main_frame()
        self.role_display = RoleDisplay(self.main_frame, self.session)

    def clear_main_frame(self):
        """Löscht alle Widgets im Hauptframe."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def run(self):
        """Startet die Anwendung."""
        self.root.mainloop()
