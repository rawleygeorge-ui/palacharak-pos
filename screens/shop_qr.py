import os
import qrcode

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty

from db import cur
from context import CURRENT_OWNER
from utils import popup


QR_FOLDER = "qr_codes"


class ShopQRScreen(Screen):

    shops = ListProperty([])
    qr_path = StringProperty("")

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

        self.qr_path = ""

        if "shop" in self.ids:
            self.ids.shop.text = "Select Shop"

    def generate_qr(self):

        shop = self.ids.shop.text

        if shop == "Select Shop":
            popup("Error", "Please select a shop")
            return

        os.makedirs(QR_FOLDER, exist_ok=True)

        file_path = os.path.join(QR_FOLDER, f"{shop}.png")

        qr = qrcode.make(shop)
        qr.save(file_path)

        self.qr_path = file_path

        popup("QR Ready", f"QR generated for shop: {shop}")

    def go_back(self):
        self.manager.current = "owner_menu"
