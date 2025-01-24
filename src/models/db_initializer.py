from sqlalchemy.orm import Session
from models.db_context import engine, Base, get_db
from models.role import Role
from models.user import User

def ensure_database_exists():
    """Erstellt die Datenbank und die Tabellen, falls sie nicht existieren."""
    print("Überprüfe, ob die Datenbank und Tabellen existieren...")
    Base.metadata.create_all(bind=engine)
    print("Datenbank und Tabellen sind bereit.")

def ensure_roles_exist():
    """Stellt sicher, dass die Standardrollen (admin, user, guest) existieren."""
    print("Überprüfe, ob die Standardrollen existieren...")
    db: Session = next(get_db())
    try:
        existing_roles = {role.name for role in db.query(Role).all()}
        required_roles = {"admin", "user", "guest"}
        missing_roles = required_roles - existing_roles

        for role_name in missing_roles:
            role = Role(name=role_name)
            db.add(role)
            print(f"Rolle '{role_name}' hinzugefügt.")

        if missing_roles:
            db.commit()
        else:
            print("Alle Standardrollen existieren bereits.")
    except Exception as e:
        print(f"Fehler beim Überprüfen der Rollen: {e}")
    finally:
        db.close()

def ensure_user_exists():
    """Stellt sicher, dass ein Benutzer mit dem Namen 'Guest' existiert."""
    print("Überprüfe, ob der Benutzer 'Guest' existiert...")
    db: Session = next(get_db())
    try:
        # Überprüfen, ob der Benutzer 'Guest' existiert
        guest_user = db.query(User).filter(User.username == "Guest").first()
        
        if not guest_user:
            # Rolle für den Benutzer sicherstellen
            guest_role = db.query(Role).filter(Role.name == "guest").first()
            if not guest_role:
                guest_role = Role(name="guest")
                db.add(guest_role)
                db.commit()
                db.refresh(guest_role)
                print("Rolle 'guest' erstellt.")

            # Benutzer 'Guest' erstellen
            guest_user = User(username="Guest", role_id=guest_role.id, rfid_key=None)
            db.add(guest_user)
            db.commit()
            print("Benutzer 'Guest' erstellt.")
        else:
            print("Benutzer 'Guest' existiert bereits.")
    except Exception as e:
        print(f"Fehler beim Überprüfen oder Erstellen des Benutzers 'Guest': {e}")
    finally:
        db.close()
