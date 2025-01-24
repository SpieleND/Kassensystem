from sqlalchemy import func
from sqlalchemy.orm import Session
from faker import Faker
from models.db_context import get_db
from models.user import User
from models.role import Role 

faker = Faker()

class UserController:
    @staticmethod
    def create_random_user():
        """Erstellt einen zufälligen Benutzer mit einer zugeordneten Rolle."""
        db: Session = next(get_db())
        try:
            username = faker.user_name()
            rfid_key = faker.uuid4()
            role = db.query(Role).order_by(func.random()).first()
            
            if not role:
                role = Role(name="Standard")
                db.add(role)
                db.commit()
                db.refresh(role)
            
            new_user = User(username=username, rfid_key=rfid_key, role_id=role.id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return f"Benutzer erstellt: {new_user.username} (RFID: {new_user.rfid_key}, Rolle: {role.name})"
        except Exception as e:
            return f"Fehler: {e}"
        finally:
            db.close()
