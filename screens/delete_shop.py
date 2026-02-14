import os

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import conn, cur
from paths import QR_DIR
from utils import popup
from context import CURRENT_OWNER


class DeleteShopScreen(Screen):
    shops = ListProperty([])

    def on_pre_enter(self):
        owner_uid = CURRENT_OWNER.get("uid")

        # 🔐 Owner session safety
        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "owner_login"
            return

        # ✅ Load ONLY this owner's shops
        self.shops = [
            r[0]
            for r in cur.execute(
                "SELECT shop_id FROM shops WHERE owner_uid=?",
                (owner_uid,),
            )
        ]

        if not self.shops:
            popup("Info", "No shops available to delete")
            self.manager.current = "owner_menu"
            return

        # Reset spinner safely
        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"

    def delete_shop(self):
        owner_uid = CURRENT_OWNER.get("uid")

        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "owner_login"
            return

        if "shop" not in self.ids:
            popup("Error", "Shop selector not found")
            return

        shop = self.ids.shop.text

        if shop == "Select Shop":
            popup("Error", "Please select a shop")
            return

        # 🔒 Extra safety: ensure shop belongs to owner
        row = cur.execute(
            "SELECT 1 FROM shops WHERE shop_id=? AND owner_uid=?",
            (shop, owner_uid),
        ).fetchone()

        if not row:
            popup("Error", "Unauthorized operation")
            return

        # Delete shop & related data
        cur.execute("DELETE FROM shops WHERE shop_id=?", (shop,))
        cur.execute("DELETE FROM users WHERE shop_id=?", (shop,))
        cur.execute("DELETE FROM inventory WHERE shop_id=?", (shop,))
        cur.execute("DELETE FROM revenue WHERE shop_id=?", (shop,))
        conn.commit()

        # Remove QR code
        qr_path = os.path.join(QR_DIR, f"{shop}.png")
        if os.path.exists(qr_path):
            os.remove(qr_path)

        popup("Deleted", f"Shop {shop} removed successfully")
        self.manager.current = "owner_menu"

    def go_back(self):
        self.manager.current = "owner_menu"
