from sqlalchemy.orm import Session
from models.db_context import get_db
from models.order import Order
from typing import List, Optional

class OrderController:
    @staticmethod
    def create_order(user_id: int, product_id: int, quantity: int) -> Optional[Order]:
        """Erstellt eine neue Bestellung."""
        db: Session = next(get_db())
        try:
            new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            return new_order
        except Exception as e:
            print(f"Fehler beim Erstellen der Bestellung: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_orders() -> List[Order]:
        """Gibt alle Bestellungen zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Order).all()
        except Exception as e:
            print(f"Fehler beim Abrufen der Bestellungen: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_order_by_id(order_id: int) -> Optional[Order]:
        """Gibt eine Bestellung basierend auf der ID zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Order).filter(Order.id == order_id).first()
        except Exception as e:
            print(f"Fehler beim Abrufen der Bestellung mit ID {order_id}: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def update_order(order_id: int, **kwargs) -> Optional[Order]:
        """Aktualisiert eine Bestellung basierend auf der ID."""
        db: Session = next(get_db())
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                print(f"Bestellung mit ID {order_id} nicht gefunden.")
                return None

            # Felder aktualisieren
            for key, value in kwargs.items():
                if hasattr(order, key):
                    setattr(order, key, value)

            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Bestellung: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def delete_order(order_id: int) -> bool:
        """Löscht eine Bestellung basierend auf der ID."""
        db: Session = next(get_db())
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                print(f"Bestellung mit ID {order_id} nicht gefunden.")
                return False

            db.delete(order)
            db.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Löschen der Bestellung: {e}")
            db.rollback()
            return False
        finally:
            db.close()
