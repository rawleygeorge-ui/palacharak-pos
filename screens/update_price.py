from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty, NumericProperty
from datetime import datetime

from db import cur, conn
from context import CURRENT_OWNER, CURRENT_POS_CONTEXT
from utils import popup


class UpdatePriceScreen(Screen):
    shops = ListProperty([])
    items = ListProperty([])
    unit = StringProperty("")
    old_price = NumericProperty(0.0)
    effective_date = StringProperty("")

    def on_pre_enter(self):

        # 🔒 BLOCK TEMP USER
        if CURRENT_POS_CONTEXT.get("source") == "user":
            popup("Access Denied", "Only owner can update prices.")
            self.manager.current = "pos"
            return

        owner_uid = CURRENT_OWNER.get("uid")
        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "login_type"
            return

        # Set system date automatically
        self.effective_date = datetime.now().strftime("%Y-%m-%d")

        self.items = []
        self.unit = ""
        self.old_price = 0.0

        self.shops = [
            r[0] for r in cur.execute(
                "SELECT shop_id FROM shops WHERE owner_uid=?",
                (owner_uid,)
            )
        ]

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"
        if "item" in self.ids:
            self.ids.item.text = "Select Item"
        if "price" in self.ids:
            self.ids.price.text = ""

    def load_items(self, shop):
        if shop == "Select Shop":
            self.items = []
            return

        self.items = [
            r[0] for r in cur.execute(
                """
                SELECT DISTINCT item
                FROM inventory
                WHERE shop_id=?
                ORDER BY LOWER(item)
                """,
                (shop,)
            )
        ]

        self.unit = ""
        self.old_price = 0.0

    def load_item_details(self, item):
        shop = self.ids.shop.text
        if shop == "Select Shop" or not item:
            return

        normalized_item = item.strip().lower()

        row = cur.execute(
            """
            SELECT unit, price
            FROM inventory
            WHERE shop_id=?
              AND LOWER(item)=?
            """,
            (shop, normalized_item)
        ).fetchone()

        if row:
            self.unit = row[0]
            self.old_price = row[1]

    def update_price(self):

        # 🔒 HARD BLOCK AT METHOD LEVEL (extra safety)
        if CURRENT_POS_CONTEXT.get("source") == "user":
            popup("Access Denied", "Only owner can update prices.")
            return

        shop = self.ids.shop.text
        item = self.ids.item.text
        price_text = self.ids.price.text.strip()

        if shop == "Select Shop" or item == "Select Item" or not price_text:
            popup("Error", "Please select shop, item, and enter new price")
            return

        try:
            new_price = float(price_text)
        except ValueError:
            popup("Error", "Invalid price value")
            return

        normalized_item = item.strip().lower()

        row = cur.execute(
            """
            SELECT unit, price
            FROM inventory
            WHERE shop_id=?
              AND LOWER(item)=?
            """,
            (shop, normalized_item)
        ).fetchone()

        if not row:
            popup("Error", "Item not found")
            return

        unit, old_price = row

        cur.execute(
            """
            INSERT INTO price_history
            (shop_id, item, unit, old_price, new_price, effective_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                shop,
                normalized_item,
                unit,
                old_price,
                new_price,
                self.effective_date,
            )
        )

        cur.execute(
            """
            UPDATE inventory
            SET price=?
            WHERE shop_id=?
              AND LOWER(item)=?
            """,
            (new_price, shop, normalized_item)
        )

        conn.commit()

        popup(
            "Price Updated",
            f"Price updated successfully\nEffective date: {self.effective_date}"
        )

        self.ids.price.text = ""

    def go_back(self):
        self.manager.current = "inventory"
