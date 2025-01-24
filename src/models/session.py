class Session:
    def __init__(self):
        self.user = None

    def set_user(self, user):
        """Setzt den aktuellen Benutzer."""
        self.user = user

    def get_user(self):
        """Gibt den aktuellen Benutzer zurück."""
        return self.user
