from models.db_initializer import ensure_database_exists, ensure_roles_exist, ensure_users_exist
from views.main_view import MainView
from utils import ROLES, session

ensure_database_exists()
ensure_roles_exist()
ensure_users_exist()

session.set_user_by_id(ROLES.guest)

if __name__ == "__main__":
    app = MainView()
    app.run()
