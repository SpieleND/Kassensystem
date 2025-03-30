from sqlalchemy.orm import Session
from models.db_context import get_db
from models.user import User
from typing import List, Optional


class UserController:
    @staticmethod
    def create_user(
        username: str,
        rfid_key: Optional[str],
        role_id: int,
        created_by: str
    ) -> Optional[User]:
        """
        Erstellt einen neuen Benutzer.

        :param username: Der Benutzername.
        :param rfid_key: Der optionale RFID-Schlüssel.
        :param role_id: Die ID der Rolle.
        :param created_by: Der Benutzer, der diesen Benutzer erstellt hat.
        :return: Das erstellte User-Objekt oder None bei Fehlern.
        """
        db: Session = next(get_db())
        try:
            new_user = User(
                username=username,
                rfid_key=rfid_key,
                role_id=role_id,
                created_by=created_by,
                updated_by=created_by  # Initially set to the creator
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            print(f"Fehler beim Erstellen des Benutzers: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_users() -> List[User]:
        """
        Gibt alle Benutzer zurück, die nicht gelöscht wurden.

        :return: Eine Liste von User-Objekten.
        """
        db: Session = next(get_db())
        try:
            return db.query(User).filter(User.is_deleted == False).all()
        except Exception as e:
            print(f"Fehler beim Abrufen der Benutzer: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Gibt einen Benutzer basierend auf seiner ID zurück.

        :param user_id: Die ID des Benutzers.
        :return: Das User-Objekt oder None, falls der Benutzer
                 nicht gefunden wurde.
        """
        db: Session = next(get_db())
        try:
            return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        except Exception as e:
            print(f"Fehler beim Abrufen des Benutzers mit ID {user_id}: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """
        Gibt einen Benutzer basierend auf seinem Benutzernamen zurück.

        :param username: Der Benutzername.
        :return: Das User-Objekt oder None, falls
                 der Benutzer nicht gefunden wurde.
        """
        db: Session = next(get_db())
        try:
            return db.query(User).filter(User.username == username, User.is_deleted == False).first()
        except Exception as e:
            print(f"Fehler beim Abrufen des Benutzers mit Benutzernamen '{username}': {e}")  # noqa: E501
            return None
        finally:
            db.close()

    @staticmethod
    def update_user(user_id: int, updated_by: str, **kwargs) -> Optional[User]:
        """
        Aktualisiert die Daten eines Benutzers.

        :param user_id: Die ID des Benutzers.
        :param updated_by: Der Benutzer, der die Änderungen vorgenommen hat.
        :param kwargs: Zu aktualisierende Felder (z. B. username, rfid_key).
        :return: Das aktualisierte User-Objekt oder None, falls der Benutzer
                 nicht gefunden wurde.
        """
        db: Session = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
            if not user:
                print(f"Benutzer mit ID {user_id} nicht gefunden.")
                return None

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.updated_by = updated_by  # Update the updated_by field
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Benutzers: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def delete_user(user_id: int, deleted_by: str) -> bool:
        """
        Markiert einen Benutzer als gelöscht.

        :param user_id: Die ID des Benutzers.
        :param deleted_by: Der Benutzer, der die Löschung vorgenommen hat.
        :return: True, wenn der Benutzer erfolgreich
                 gelöscht wurde, sonst False.
        """
        db: Session = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
            if not user:
                print(f"Benutzer mit ID {user_id} nicht gefunden.")
                return False

            user.is_deleted = True
            user.updated_by = deleted_by  # Update the updated_by field
            db.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Löschen des Benutzers: {e}")
            db.rollback()
            return False
        finally:
            db.close()
