from controllers.user_controller import UserController

class Session:
    def __init__(self):
        self.user = None

    def set_user_by_id(self, user_id):
        """Setzt den aktuellen Benutzer."""
        self.user = UserController.get_user_by_id(user_id)

    def get_user(self):
        """Gibt den aktuellen Benutzer zurück."""
        return self.user
