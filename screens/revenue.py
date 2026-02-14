########################################################
# Revenue.py
########################################################

from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from db import conn, cur
from utils import popup
from context import CURRENT_OWNER


class RevenueScreen(Screen):
    shops = ListProperty([])

    def on_pre_enter(self):

        owner_uid = CURRENT_OWNER.get("uid")

        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "login_type"
            return

        # Load ONLY shops for this owner
        self.shops = [
            r[0] for r in cur.execute(
                "SELECT shop_id FROM shops WHERE owner_uid=?",
                (owner_uid,),
            )
        ]

        if not self.shops:
            popup("Info", "No shops available. Create a shop first.")
            self.manager.current = "owner_menu"
            return

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"

        if "date" in self.ids:
            self.ids.date.text = datetime.now().strftime("%Y-%m-%d")

        if "particulars" in self.ids:
            self.ids.particulars.text = "Select Particulars"

        for field in ["desc", "amount"]:
            if field in self.ids:
                self.ids[field].text = ""

    def add_record(self):

        shop = self.ids.shop.text
        date = self.ids.date.text.strip()
        particulars = self.ids.particulars.text.strip()
        desc = self.ids.desc.text.strip()
        amount_text = self.ids.amount.text.strip()

        if shop == "Select Shop":
            popup("Error", "Please select a shop")
            return

        if particulars == "Select Particulars":
            popup("Error", "Please select particulars")
            return

        if not all([date, amount_text]):
            popup("Error", "Date and amount are required")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            popup("Error", "Invalid amount")
            return

        existing = cur.execute(
            """
            SELECT 1 FROM revenue
            WHERE shop_id=? AND date=? AND particulars=? AND amount=?
            """,
            (shop, date, particulars, amount),
        ).fetchone()

        if existing:
            popup("Info", "This revenue record already exists")
            return

        cur.execute(
            """
            INSERT INTO revenue (shop_id, date, particulars, description, amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (shop, date, particulars, desc, amount),
        )
        conn.commit()

        popup("Saved", "Revenue record added")

        self.ids.particulars.text = "Select Particulars"
        self.ids.desc.text = ""
        self.ids.amount.text = ""
