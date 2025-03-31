from tkinter import Tk, Frame
import os
from utils import ROLES, session
from views.admin_view import AdminView


class MainView:
    def __init__(self):
        """Initialisiert die Hauptansicht."""
        self.root = Tk()
        self.root.title("Komponentenbasierte View")
        self.root.geometry(os.getenv("DISPLAY_RESOLUTION"))

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.admin_view = AdminView(self.main_frame, self.logout)

        # Standardansicht anzeigen
        self.admin_view.show_role_display()

        # Tastenkürzel für Admin-Modus
        self.root.bind("<l>", self.enter_admin_mode)

    def enter_admin_mode(self, event=None):
        """Wechselt in den administrativen Bereich."""
        session.set_user_by_id(ROLES.admin)
        self.admin_view.show_admin_menu()

    def logout(self):
        """Wechselt zurück in den Standardmodus."""
        session.set_user_by_id(ROLES.guest)
        self.admin_view.show_role_display()

    def run(self):
        """Startet die Anwendung."""
        self.root.mainloop()
