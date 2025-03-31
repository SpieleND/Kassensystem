from tkinter import Frame
from views.components.admin_menu import AdminMenu
from views.components.role_display import RoleDisplay

class AdminView:
    def __init__(self, parent, logout_callback):
        """Initialisiert die Admin-Ansicht."""
        self.parent = parent
        self.logout_callback = logout_callback
        self.admin_menu = None

    def show_admin_menu(self):
        """Zeigt das Admin-Menü an."""
        self.clear_parent()
        self.admin_menu = AdminMenu(self.parent, self.logout_callback)

    def show_role_display(self):
        """Zeigt die Rollenanzeige an."""
        self.clear_parent()
        RoleDisplay(self.parent)

    def clear_parent(self):
        """Löscht alle Widgets im übergeordneten Frame."""
        for widget in self.parent.winfo_children():
            widget.destroy()