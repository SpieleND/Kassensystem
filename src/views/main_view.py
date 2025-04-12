from tkinter import Tk, Frame, Button
import os
from utils import ROLES, session
from views.admin_view import AdminView
from models.db_context import get_db
from models.product import Product


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
        self.show_products()

        # Tastenkürzel für Admin-Modus
        self.root.bind("<l>", self.enter_admin_mode)

    def show_products(self):
        """Zeigt die Produkte als Buttons an."""
        self.clear_main_frame()
        db = next(get_db())
        try:
            # Filter products where is_deleted is False
            products = db.query(Product).filter(Product.is_deleted == False).all()
            for product in products:
                button = Button(
                    self.main_frame,
                    text=product.name,
                    command=lambda p=product: self.on_product_click(p)
                )
                button.pack(pady=5)  # Adjust layout as needed
        except Exception as e:
            print(f"Fehler beim Abrufen der Produkte: {e}")
        finally:
            db.close()

    def on_product_click(self, product):
        """Wird aufgerufen, wenn ein Produkt-Button geklickt wird."""
        print(f"Produkt '{product.name}' wurde geklickt.")
        # Hier können Sie die gewünschte Logik implementieren

    def clear_main_frame(self):
        """Löscht alle Widgets im Haupt-Frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    def enter_admin_mode(self, event=None):
        """Wechselt in den administrativen Bereich."""
        session.set_user_by_id(ROLES.admin)
        self.admin_view.show_admin_menu()

    def logout(self):
        """Wechselt zurück in den Standardmodus."""
        session.set_user_by_id(ROLES.guest)
        self.show_products()

    def run(self):
        """Startet die Anwendung."""
        self.root.mainloop()
