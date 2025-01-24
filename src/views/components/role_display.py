from tkinter import Label

class RoleDisplay:
    def __init__(self, parent, session):
        """Zeigt die Rolle des aktuellen Benutzers oder 'Guest' an."""
        self.session = session
        self.label = Label(parent, text=self._get_display_text())
        self.label.pack(pady=20)

    def _get_display_text(self):
        """Gibt den Text basierend auf dem aktuellen Benutzer zurück."""
        user = self.session.get_user()
        if user and user.role:
            return f"Rolle: {user.role.name}"
        return "Rolle: Guest"  

    def update(self):
        """Aktualisiert die Anzeige."""
        self.label.config(text=self._get_display_text())
