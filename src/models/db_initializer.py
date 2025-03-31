from enum import Enum
from sqlalchemy.orm import Session
from models.db_context import engine, Base, get_db
from models.role import Role
from models.user import User
from models.product import Product
from models.order import Order


class RoleEnum(Enum):
    SYSTEM = "system"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


roles_to_create = {role.value for role in RoleEnum}

users_to_create = [
    {"username": "SYSTEM", "role_enum": RoleEnum.SYSTEM, "created_by": "SYSTEM", "updated_by": "SYSTEM"},
    {"username": "Admin", "role_enum": RoleEnum.ADMIN, "created_by": "SYSTEM", "updated_by": "SYSTEM"},
    {"username": "Guest", "role_enum": RoleEnum.GUEST, "created_by": "SYSTEM", "updated_by": "SYSTEM"},
]


def ensure_database_exists():
    """Erstellt die Datenbank und die Tabellen, falls sie nicht existieren."""
    print("Überprüfe, ob die Datenbank und Tabellen existieren...")
    Base.metadata.create_all(bind=engine)
    print("Datenbank und Tabellen sind bereit.")


def ensure_roles_exist():
    """Stellt sicher, dass die Standardrollen
    (admin, user, guest) existieren."""
    print("Überprüfe, ob die Standardrollen existieren...")
    db: Session = next(get_db())
    try:
        existing_roles = {role.name for role in db.query(Role).all()}
        missing_roles = roles_to_create - existing_roles

        for role_name in RoleEnum:
            if role_name.value not in existing_roles:
                role = Role(name=role_name.value)
                db.add(role)
                print(f"Rolle '{role_name.value}' hinzugefügt.")

        if missing_roles:
            db.commit()
        else:
            print("Alle Standardrollen existieren bereits.")
    except Exception as e:
        print(f"Fehler beim Überprüfen der Rollen: {e}")
    finally:
        db.close()


def ensure_users_exist():
    """Stellt sicher, dass die Benutzer 'SYSTEM', 'Admin' und 'Guest' existieren."""
    print("Überprüfe, ob die Benutzer 'SYSTEM', 'Admin' und 'Guest' existieren...")
    db: Session = next(get_db())
    try:
        for user_info in users_to_create:
            # Überprüfen, ob der Benutzer existiert
            user = db.query(User).filter(User.username == user_info["username"]).first()

            if not user:
                # Rolle anhand von RoleEnum abrufen
                role = db.query(Role).filter(Role.name == user_info["role_enum"].value).first()
                if not role:
                    raise ValueError(f"Rolle '{user_info['role_enum'].value}' existiert nicht in der Datenbank.")

                # Benutzer erstellen
                user = User(
                    username=user_info["username"],
                    role_id=role.id,
                    rfid_key=None,
                    created_by=user_info["created_by"],
                    updated_by=user_info["updated_by"]
                )
                db.add(user)
                db.commit()
                print(f"Benutzer '{user_info['username']}' erstellt.")
            else:
                print(f"Benutzer '{user_info['username']}' existiert bereits.")
    except Exception as e:
        print(f"Fehler beim Überprüfen oder Erstellen der Benutzer: {e}")
    finally:
        db.close()
