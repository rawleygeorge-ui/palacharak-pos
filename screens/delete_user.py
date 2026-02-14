from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import cur, conn
from utils import popup
from context import CURRENT_OWNER


class DeleteUserScreen(Screen):
    shops = ListProperty([])
    users = ListProperty([])

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

        self.users = []

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"

        if "user" in self.ids:
            self.ids.user.text = "Select User"

        if not self.shops:
            popup("Info", "No shops available for this owner.")
            self.manager.current = "owner_menu"

    def load_users(self, shop):
        if shop == "Select Shop":
            self.users = []
            return

        self.users = [
            r[0]
            for r in cur.execute(
                "SELECT username FROM users WHERE shop_id=?",
                (shop,),
            )
        ]

        if not self.users:
            popup("Info", "No users found for this shop.")

    def delete_user(self):
        shop = self.ids.shop.text
        user = self.ids.user.text

        if shop == "Select Shop" or user == "Select User":
            popup("Error", "Select both shop and user")
            return

        cur.execute(
            "DELETE FROM users WHERE shop_id=? AND username=?",
            (shop, user),
        )
        conn.commit()

        popup("Deleted", f"User '{user}' removed")

        # Refresh user list
        self.load_users(shop)

        if "user" in self.ids:
            self.ids.user.text = "Select User"
