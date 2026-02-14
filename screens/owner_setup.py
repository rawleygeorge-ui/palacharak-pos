import json
from kivy.uix.screenmanager import Screen

from paths import OWNER_FILE
from utils import popup


class OwnerSetupScreen(Screen):
    def save_owner(self):
        uid = self.ids.uid.text.strip()
        pwd = self.ids.pwd.text.strip()

        if not uid or not pwd:
            popup("Error", "Enter User ID & Password")
            return

        with open(OWNER_FILE, "w") as f:
            json.dump(
                {
                    "uid": uid,
                    "pwd": pwd
                },
                f,
            )

        popup("Saved", "Owner created. Please login.")
        self.manager.current = "owner_login"
