from models.db_initializer import ensure_database_exists, ensure_roles_exist, ensure_users_exist
from models.session import Session
from views.main_view import MainView

session = Session()

if __name__ == "__main__":
    ensure_database_exists()
    ensure_roles_exist()
    ensure_users_exist()
    app = MainView(session)
    app.run()
