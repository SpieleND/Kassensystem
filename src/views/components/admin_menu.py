from tkinter import Frame, Button
from views.components.product_management import ProductManagement

class AdminMenu:
    def __init__(self, parent, session, logout_callback):
        """Initialisiert das Admin-Menü."""
        self.frame = Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # Produktverwaltung
        self.product_management = ProductManagement(self.frame)

        # Logout-Button
        logout_button = Button(self.frame, text="Logout", command=logout_callback)
        logout_button.pack(side="bottom", pady=10)
