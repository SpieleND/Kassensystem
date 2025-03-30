from sqlalchemy.orm import Session
from models.db_context import get_db
from models.role import Role
from typing import List, Optional


class RoleController:
    @staticmethod
    def get_all_roles() -> List[Role]:
        """Gibt alle Rollen zurück, die nicht gelöscht wurden."""
        db: Session = next(get_db())
        try:
            return db.query(Role).filter(Role.is_deleted == False).all()
        except Exception as e:
            print(f"Fehler beim Abrufen aller Rollen: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[Role]:
        """Gibt eine Rolle basierend auf ihrer ID zurück."""
        db: Session = next(get_db())
        try:
            return db.query(Role).filter(Role.id == role_id, Role.is_deleted == False).first()
        except Exception as e:
            print(f"Fehler beim Abrufen der Rolle mit ID {role_id}: {e}")
            return None
        finally:
            db.close()
