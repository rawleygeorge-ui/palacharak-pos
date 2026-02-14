from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.label import Label

from db import cur, conn
from utils import popup
from context import CURRENT_POS_CONTEXT, CURRENT_OWNER


class POSScreen(Screen):
    shops = ListProperty([])
    items = ListProperty([])
    total = NumericProperty(0.0)

    def on_pre_enter(self):
        # 🔑 HARD RESET (prevents duplication)
        self.cart = []
        self.total = 0.0

        if "total" in self.ids:
            self.ids.total.text = "0.00"

        if "cart_grid" in self.ids:
            self.ids.cart_grid.clear_widgets()

        source = CURRENT_POS_CONTEXT.get("source")

        # ---------- USER FLOW ----------
        if source == "user":
            shop = CURRENT_POS_CONTEXT.get("shop")
            if shop:
                self.ids.shop.text = shop
                self.load_items(shop)
            return

        # ---------- OWNER FLOW ----------
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

        self.ids.shop.text = "Select Shop"
        self.items = []

    def load_items(self, shop):
        if shop == "Select Shop":
            self.items = []
            return

        self.items = [
            r[0] for r in cur.execute(
                "SELECT item FROM inventory WHERE shop_id=?",
                (shop,)
            )
        ]

    def add_item(self):
        shop = self.ids.shop.text
        item = self.ids.item.text
        qty_text = self.ids.qty.text.strip()

        if shop == "Select Shop" or item == "Select Item" or not qty_text:
            popup("Error", "Select shop, item and quantity")
            return

        try:
            qty = float(qty_text)
            if qty <= 0:
                raise ValueError
        except ValueError:
            popup("Error", "Invalid quantity")
            return

        row = cur.execute(
            "SELECT price FROM inventory WHERE shop_id=? AND item=?",
            (shop, item),
        ).fetchone()

        if not row:
            popup("Error", "Item price not found")
            return

        price = row[0]
        line_total = price * qty

        # 🔑 INTERNAL CART (NOT UI-BOUND)
        self.cart.append({
            "item": item,
            "qty": qty,
            "amount": line_total
        })

        # 🔢 UPDATE TOTAL
        self.total += line_total
        self.ids.total.text = f"{self.total:.2f}"

        # 🔁 UI GRID UPDATE
        grid = self.ids.cart_grid
        grid.add_widget(Label(text=item))
        grid.add_widget(Label(text=str(qty)))
        grid.add_widget(Label(text=f"{line_total:.2f}"))

        self.ids.qty.text = ""
        self.ids.item.text = "Select Item"

    def finalize_bill(self):
        if not self.cart:
            popup("Error", "Cart is empty")
            return

        shop = self.ids.shop.text
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # 🧾 GENERATE SIMPLE BILL NUMBER
        bill_no = f"POS-{timestamp}"

        # ✅ INSERT ONE LEDGER ENTRY PER BILL
        cur.execute(
            """
            INSERT INTO revenue (shop_id, date, particulars, description, amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                shop,
                today,
                "Income",
                f"Bill No: {bill_no}",
                self.total
            )
        )

        conn.commit()

        popup(
            "Bill Saved",
            f"Bill No: {bill_no}\nTotal Amount: ₹{self.total:.2f}"
        )

        # 🔁 RESET (prevents duplication)
        self.cart = []
        self.total = 0.0
        self.ids.total.text = "0.00"
        self.ids.cart_grid.clear_widgets()

    def go_back(self):
        src = CURRENT_POS_CONTEXT.get("source")
        CURRENT_POS_CONTEXT.clear()

        self.manager.current = (
            "user_login" if src == "user" else "owner_menu"
        )
