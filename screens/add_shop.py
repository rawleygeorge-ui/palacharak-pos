import os
import qrcode

from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

from db import conn, cur
from paths import QR_DIR
from utils import popup
from context import CURRENT_OWNER


class AddShopScreen(Screen):
    enabled = BooleanProperty(False)

    def on_pre_enter(self):
        # 🔐 Hard safety check
        if not CURRENT_OWNER.get("uid"):
            popup("Session Expired", "Please login again")
            self.manager.current = "owner_login"
            return

        # Reset fields safely
        for field in ["shop", "owner", "dob", "mobile", "town"]:
            if field in self.ids:
                self.ids[field].text = ""

        self.enabled = False

    def validate(self):
        self.enabled = all(
            self.ids[x].text.strip()
            for x in ["shop", "owner", "dob", "mobile", "town"]
        )

    def create_shop(self):
        owner_uid = CURRENT_OWNER.get("uid")

        if not owner_uid:
            popup("Session Expired", "Please login again")
            self.manager.current = "owner_login"
            return

        shop = self.ids.shop.text.strip()
        owner = self.ids.owner.text.strip()
        dob = self.ids.dob.text.strip()
        mobile = self.ids.mobile.text.strip()
        town = self.ids.town.text.strip()

        if not all([shop, owner, dob, mobile, town]):
            popup("Error", "All fields are required")
            return

        shop_id = (
            shop[:4] + owner[:4] + dob[:4] + town[:4] + mobile
        ).upper()

        cur.execute(
            """
            INSERT INTO shops
            (shop_id, shop_name, owner_name, dob, mobile, town, owner_uid)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (shop_id, shop, owner, dob, mobile, town, owner_uid),
        )
        conn.commit()

        qr_path = os.path.join(QR_DIR, f"{shop_id}.png")
        if not os.path.exists(qr_path):
            qrcode.make(shop_id).save(qr_path)

        popup("Success", f"Shop {shop_id} created")
        self.manager.current = "owner_menu"
