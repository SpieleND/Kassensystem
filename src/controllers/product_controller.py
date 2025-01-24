from sqlalchemy.orm import Session
from models.db_context import get_db
from models.product import Product

class ProductController:
    @staticmethod
    def create_product(name, description, price):
        """Erstellt ein neues Produkt."""
        db: Session = next(get_db())
        try:
            new_product = Product(name=name, description=description, price=price)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return new_product
        except Exception as e:
            print(f"Fehler beim Erstellen des Produkts: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_products():
        """Gibt alle Produkte zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Product).all()
        except Exception as e:
            print(f"Fehler beim Abrufen der Produkte: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_product_by_id(product_id):
        """Gibt ein Produkt basierend auf der ID zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Product).filter(Product.id == product_id).first()
        except Exception as e:
            print(f"Fehler beim Abrufen des Produkts: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def update_product(product_id, name=None, description=None, price=None):
        """Aktualisiert ein bestehendes Produkt."""
        db: Session = next(get_db())
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                print("Produkt nicht gefunden.")
                return None

            if name:
                product.name = name
            if description:
                product.description = description
            if price is not None:
                product.price = price

            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Produkts: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def delete_product(product_id):
        """Löscht ein Produkt basierend auf der ID."""
        db: Session = next(get_db())
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                print("Produkt nicht gefunden.")
                return False

            db.delete(product)
            db.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Löschen des Produkts: {e}")
            db.rollback()
            return False
        finally:
            db.close()
