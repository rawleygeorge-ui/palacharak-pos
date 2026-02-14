from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class QRScanScreen(Screen):

    def on_enter(self):
        # small delay so camera initializes cleanly
        Clock.schedule_once(self.start_scanner, 0.5)

    def start_scanner(self, dt):
        self.ids.zbarcam.start()

    def on_qr_detected(self, instance, value):
        if value:
            shop_id = value.strip().upper()

            # Send scanned shop_id back to login screen
            login_screen = self.manager.get_screen("user_login")
            login_screen.set_shop_from_qr(shop_id)

            self.ids.zbarcam.stop()
