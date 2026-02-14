from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import cur, conn
from utils import popup
from context import CURRENT_OWNER


class AddUserScreen(Screen):
    shops = ListProperty([])

    def on_pre_enter(self):
        owner_uid = CURRENT_OWNER.get("uid")

        if not owner_uid:
            popup("Error", "Owner session not found. Please login again.")
            self.manager.current = "owner_login"
            return

        # ✅ Load only this owner's shops
        self.shops = [
            r[0]
            for r in cur.execute(
                "SELECT shop_id FROM shops WHERE owner_uid=?",
                (owner_uid,),
            )
        ]

        # Reset input
        if "username" in self.ids:
            self.ids.username.text = ""

        if not self.shops:
            popup("Info", "No shops available for this owner.")
            self.manager.current = "owner_menu"

    def add_user(self):
        shop = self.ids.shop.text
        user = self.ids.username.text.strip()

        if shop == "Select Shop" or not user:
            popup("Error", "Please select a shop and enter a username")
            return

        cur.execute(
            "INSERT INTO users (shop_id, username) VALUES (?, ?)",
            (shop, user),
        )
        conn.commit()

        popup("Success", f"User '{user}' added")
        self.ids.username.text = ""
