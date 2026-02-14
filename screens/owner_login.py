import os
import json

from kivy.uix.screenmanager import Screen

from paths import OWNER_FILE
from utils import popup
from context import CURRENT_OWNER


class OwnerLoginScreen(Screen):
    def on_pre_enter(self):
        if "error" in self.ids:
            self.ids.error.text = ""
        if "create_btn" in self.ids:
            self.ids.create_btn.opacity = 0
            self.ids.create_btn.disabled = True

    def login(self):
        if not os.path.exists(OWNER_FILE):
            popup("Info", "Owner not set up yet. Please create one.")
            self.manager.current = "owner_setup"
            return

        with open(OWNER_FILE, "r") as f:
            data = json.load(f)

        uid = self.ids.uid.text.strip()
        pwd = self.ids.pwd.text.strip()

        if uid == data.get("uid") and pwd == data.get("pwd"):
            CURRENT_OWNER["uid"] = uid
            self.manager.current = "owner_menu"
        else:
            if "error" in self.ids:
                self.ids.error.text = (
                    "Invalid Owner credentials.\n"
                    "Select 'Create New Owner' to create one."
                )
            if "create_btn" in self.ids:
                self.ids.create_btn.opacity = 1
                self.ids.create_btn.disabled = False

    def create_new_owner(self):
        self.manager.current = "owner_setup"
