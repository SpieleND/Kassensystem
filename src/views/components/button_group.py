from tkinter import Button

class ButtonGroup:
    def __init__(self, parent, actions):
        """
        Erstellt eine Gruppe von Buttons.
        :param parent: Der übergeordnete Frame oder das Fenster.
        :param actions: Liste von Aktionen, z. B. [{"text": "Logout", "command": ...}, ...]
        """
        self.buttons = []
        for action in actions:
            button = Button(parent, text=action["text"], command=action["command"])
            button.pack(pady=5)
            self.buttons.append(button)
