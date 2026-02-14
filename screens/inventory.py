from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import cur, conn
from utils import popup
from context import CURRENT_OWNER, CURRENT_POS_CONTEXT


class InventoryScreen(Screen):
    shops = ListProperty([])

    def on_pre_enter(self):

        # 🔒 BLOCK TEMP USER
        if CURRENT_POS_CONTEXT.get("source") == "user":
            popup("Access Denied", "Only owner can access inventory.")
            self.manager.current = "pos"
            return

        owner_uid = CURRENT_OWNER.get("uid")

        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "login_type"
            return

        self.shops = [
            r[0] for r in cur.execute(
                "SELECT shop_id FROM shops WHERE owner_uid=?",
                (owner_uid,)
            )
        ]

        if not self.shops:
            popup("Info", "No shops available")
            self.manager.current = "owner_menu"
            return

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"

        if "item" in self.ids:
            self.ids.item.text = ""

        if "unit" in self.ids:
            self.ids.unit.text = "Select Unit"

        if "price" in self.ids:
            self.ids.price.text = ""

    def add_item(self):

        # 🔒 EXTRA SAFETY
        if CURRENT_POS_CONTEXT.get("source") == "user":
            popup("Access Denied", "Only owner can add items.")
            return

        shop = self.ids.shop.text
        item = self.ids.item.text.strip()
        unit = self.ids.unit.text
        price = self.ids.price.text.strip()

        if (
            shop == "Select Shop"
            or not item
            or unit == "Select Unit"
            or not price
        ):
            popup("Error", "All fields are required")
            return

        try:
            price = float(price)
        except ValueError:
            popup("Error", "Invalid price")
            return

        exists = cur.execute(
            """
            SELECT 1 FROM inventory
            WHERE shop_id = ?
              AND LOWER(item) = LOWER(?)
            """,
            (shop, item),
        ).fetchone()

        if exists:
            popup(
                "Duplicate Item",
                f"'{item}' already exists.\n"
                "Use a different Item name."
            )
            return

        cur.execute(
            """
            INSERT INTO inventory (shop_id, item, unit, price)
            VALUES (?, ?, ?, ?)
            """,
            (shop, item, unit, price),
        )
        conn.commit()

        popup("Saved", f"Item '{item}' added")

        self.ids.item.text = ""
        self.ids.unit.text = "Select Unit"
        self.ids.price.text = ""
