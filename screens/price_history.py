from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import cur
from context import CURRENT_OWNER
from utils import popup


class PriceHistoryScreen(Screen):
    shops = ListProperty([])
    items = ListProperty([])
    records = ListProperty([])   # reserved for future
    rv_data = ListProperty([])

    def on_pre_enter(self):
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

        self.items = []
        self.records = []
        self.rv_data = []

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"
        if "item" in self.ids:
            self.ids.item.text = "Select Item"

    def load_items(self, shop):
        if shop == "Select Shop":
            self.items = []
            self.records = []
            self.rv_data = []
            return

        self.items = [
            r[0] for r in cur.execute(
                "SELECT DISTINCT item FROM inventory WHERE shop_id=?",
                (shop,)
            )
        ]

        self.records = []
        self.rv_data = []

    def load_history(self, item):
        shop = self.ids.shop.text

        if shop == "Select Shop" or item == "Select Item":
            self.rv_data = []
            return

        row = cur.execute(
            """
            SELECT new_price, effective_date, unit
            FROM price_history
            WHERE shop_id=? AND item=?
            ORDER BY rowid DESC
            LIMIT 2
            """,
            (shop, item)
        ).fetchall()

        if not row:
            popup("Info", "No price history available")
            self.rv_data = []
            return

        latest_price, latest_date, unit = row[0]
        previous_price = row[1][0] if len(row) > 1 else "—"

        self.rv_data = [{
            "item": item,
            "old_price": f"{previous_price} ({unit})",
            "new_price": f"{latest_price} ({unit})",
            "date": latest_date,
        }]
