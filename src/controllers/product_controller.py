from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.db_context import get_db
from models.product import Product
from typing import List, Optional


class ProductController:
    @staticmethod
    def create_product(
        name: str,
        price: float,
        created_by: str
    ) -> Optional[Product]:
        """Erstellt ein neues Produkt."""
        db: Session = next(get_db())
        try:
            new_product = Product(
                name=name,
                price=price,
                created_by=created_by,
                updated_by=created_by  # Set initially to the creator
            )
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
    def get_all_products() -> List[Product]:
        """Gibt alle Produkte zurück, die nicht gelöscht wurden."""
        db: Session = next(get_db())
        try:
            return db.query(Product).filter(Product.is_deleted == False).all()
        except Exception as e:
            print(f"Fehler beim Abrufen der Produkte: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Gibt ein Produkt basierend auf der ID zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
        except Exception as e:
            print(f"Fehler beim Abrufen des Produkts: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def update_product(
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        updated_by: str = None
    ) -> Optional[Product]:
        """Aktualisiert ein bestehendes Produkt."""
        db: Session = next(get_db())
        try:
            product = (
                db.query(Product)
                .filter(Product.id == product_id, Product.is_deleted == False)
                .first()
            )
            if not product:
                print("Produkt nicht gefunden.")
                return None

            if name:
                product.name = name
            if price is not None:
                product.price = price
            if updated_by:
                product.updated_by = updated_by

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
    def delete_product(product_id: int, deleted_by: str) -> bool:
        """Markiert ein Produkt als gelöscht."""
        db: Session = next(get_db())
        try:
            product = (
                db.query(Product)
                .filter(Product.id == product_id, Product.is_deleted == False)
                .first()
            )
            if not product:
                print("Produkt nicht gefunden.")
                return False

            product.is_deleted = True
            product.updated_by = deleted_by

            db.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Löschen des Produkts: {e}")
            db.rollback()
            return False
        finally:
            db.close()
