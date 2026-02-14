from kivy.uix.screenmanager import Screen
from utils import popup
from context import CURRENT_POS_CONTEXT
from db import cur


class UserLoginScreen(Screen):

    def open_scanner(self):
        self.manager.current = "qr_scan"

    def set_shop_from_qr(self, shop_id):
        """
        Called by QR scanner screen after successful scan
        """
        self.ids.shop_id.text = shop_id
        self.manager.current = "user_login"

    def login(self):
        shop_input = self.ids.shop_id.text.strip().upper()
        user_input = self.ids.user_id.text.strip()

        if not shop_input or not user_input:
            popup("Error", "Enter Shop ID and Username")
            return

        row = cur.execute(
            """
            SELECT shop_id FROM users 
            WHERE username=? AND shop_id=?
            """,
            (user_input, shop_input)
        ).fetchone()

        if not row:
            popup("Error", "Invalid Shop ID or Username")
            return

        CURRENT_POS_CONTEXT.clear()
        CURRENT_POS_CONTEXT["source"] = "user"
        CURRENT_POS_CONTEXT["shop"] = shop_input

        self.manager.current = "pos"
