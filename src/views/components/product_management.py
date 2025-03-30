from tkinter import Frame, Button, Label, Listbox, Toplevel, Entry
from controllers.product_controller import ProductController

class ProductManagement:
    def __init__(self, parent):
        """Erstellt den Bereich für die Produktverwaltung."""
        self.frame = Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Produktliste
        Label(self.frame, text="Produkte:").pack(anchor="w")
        self.product_listbox = Listbox(self.frame, height=10, width=50)
        self.product_listbox.pack(pady=5)

        # Buttons für CRUD-Operationen
        Button(self.frame, text="Produkt hinzufügen", command=self.add_product).pack(side="left", padx=5)
        Button(self.frame, text="Produkt bearbeiten", command=self.edit_product).pack(side="left", padx=5)
        Button(self.frame, text="Produkt löschen", command=self.delete_product).pack(side="left", padx=5)

        # Produkte laden
        self.load_products()

    def load_products(self):
        """Lädt alle Produkte in die Liste."""
        self.product_listbox.delete(0, "end")  # Liste leeren
        products = ProductController.get_all_products()
        for product in products:
            self.product_listbox.insert(
                "end",
                f"{product.id}: {product.name} - {product.price} € (Erstellt von: {product.created_by})"
            )

    def add_product(self):
        """Öffnet ein Dialogfenster zum Hinzufügen eines Produkts."""
        self._show_product_dialog("Neues Produkt hinzufügen", self._create_product)

    def edit_product(self):
        """Öffnet ein Dialogfenster zum Bearbeiten eines Produkts."""
        selected = self._get_selected_product()
        if not selected:
            return

        product_id = int(selected.split(":")[0])  # ID aus der Auswahl extrahieren
        product = ProductController.get_product_by_id(product_id)

        if product:
            self._show_product_dialog(
                "Produkt bearbeiten",
                lambda name, price: self._update_product(product.id, name, price),
                product
            )

    def delete_product(self):
        """Löscht das ausgewählte Produkt."""
        selected = self._get_selected_product()
        if not selected:
            return

        product_id = int(selected.split(":")[0])  # ID aus der Auswahl extrahieren
        success = ProductController.delete_product(product_id, deleted_by="Admin")  # Replace "Admin" with the actual user
        if success:
            self.load_products()

    def _get_selected_product(self):
        """Gibt das ausgewählte Produkt aus der Liste zurück."""
        try:
            return self.product_listbox.get(self.product_listbox.curselection())
        except:
            print("Kein Produkt ausgewählt.")
            return None

    def _show_product_dialog(self, title, on_submit, product=None):
        """Zeigt ein Dialogfenster für Produktoperationen."""
        dialog = Toplevel(self.frame)
        dialog.title(title)

        Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        Label(dialog, text="Preis:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        price_entry = Entry(dialog, width=30)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        if product:
            name_entry.insert(0, product.name)
            price_entry.insert(0, str(product.price))

        def submit():
            name = name_entry.get()
            try:
                price = float(price_entry.get())
            except ValueError:
                print("Ungültiger Preis.")
                return

            on_submit(name, price)
            dialog.destroy()
            self.load_products()

        Button(dialog, text="Speichern", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

    def _create_product(self, name, price):
        """Erstellt ein neues Produkt."""
        ProductController.create_product(name, price, created_by="Admin")  # Replace "Admin" with the actual user

    def _update_product(self, product_id, name, price):
        """Aktualisiert ein bestehendes Produkt."""
        ProductController.update_product(product_id, name, price, updated_by="Admin")  # Replace "Admin" with the actual user
