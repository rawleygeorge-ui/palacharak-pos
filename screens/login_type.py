from kivy.uix.screenmanager import Screen
import os

from paths import OWNER_FILE


class LoginTypeScreen(Screen):
    def go_owner(self):
        """
        If owner is not created yet → go to owner setup
        Else → go to owner login
        """
        if not os.path.exists(OWNER_FILE):
            self.manager.current = "owner_setup"
        else:
            self.manager.current = "owner_login"

    def go_user(self):
        """
        User login flow
        """
        self.manager.current = "user_login"
