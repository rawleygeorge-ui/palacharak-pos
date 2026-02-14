#########################################
# Ledger.py
#########################################

from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label

from db import cur
from utils import popup


class LedgerScreen(Screen):
    title_text = StringProperty("")

    def on_pre_enter(self):
        print(">>> ENTERING LEDGER SCREEN")

        today = datetime.now().strftime("%Y-%m-%d")
        self.title_text = f"Daily Ledger for {today}"

        self.load_ledger(today)

    def load_ledger(self, date):

        if "ledger_grid" not in self.ids:
            print("❌ ledger_grid not found in KV")
            return

        grid = self.ids.ledger_grid
        grid.clear_widgets()

        revenue_screen = self.manager.get_screen("revenue")

        if "shop" not in revenue_screen.ids:
            popup("Error", "Shop selection not available")
            return

        shop = revenue_screen.ids.shop.text

        if not shop or shop == "Select Shop":
            popup("Error", "Please select a shop first")
            return

        rows = cur.execute(
            """
            SELECT description, particulars, amount
            FROM revenue
            WHERE shop_id = ? AND date = ?
            ORDER BY rowid
            """,
            (shop, date),
        ).fetchall()

        if not rows:
            grid.add_widget(Label(text="-"))
            grid.add_widget(Label(text="No entries"))
            grid.add_widget(Label(text="-"))
            grid.add_widget(Label(text="-"))
            grid.add_widget(Label(text="-"))
            grid.add_widget(Label(text="0.00"))
            return

        balance = 0.0
        slno = 1

        for description, particulars, amount in rows:

            debit = ""
            credit = ""
            sign = ""

            if particulars == "Expense":
                debit = f"{amount:.2f}"
                balance -= amount
                sign = "-"
            else:
                credit = f"{amount:.2f}"
                balance += amount
                sign = "+"

            # Create colored labels
            sl_label = Label(text=str(slno))
            desc_label = Label(text=description)
            sign_label = Label(text=sign)

            debit_label = Label(
                text=debit,
                color=(1, 0, 0, 1) if debit else (1, 1, 1, 1)
            )

            credit_label = Label(
                text=credit,
                color=(0, 1, 0, 1) if credit else (1, 1, 1, 1)
            )

            balance_label = Label(text=f"{balance:.2f}")

            widgets = [
                sl_label,
                desc_label,
                sign_label,
                debit_label,
                credit_label,
                balance_label,
            ]

            for w in widgets:
                grid.add_widget(w)

            slno += 1
