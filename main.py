from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# -------------------------------------------------
# IMPORT ALL SCREENS
# -------------------------------------------------
from screens.splash import SplashScreen
from screens.login_type import LoginTypeScreen
from screens.owner_setup import OwnerSetupScreen
from screens.owner_login import OwnerLoginScreen
from screens.owner_menu import OwnerMenuScreen

from screens.add_shop import AddShopScreen
from screens.delete_shop import DeleteShopScreen
from screens.add_user import AddUserScreen
from screens.delete_user import DeleteUserScreen
from screens.qr_scan import QRScanScreen


from screens.inventory import InventoryScreen
from screens.update_price import UpdatePriceScreen
from screens.price_history import PriceHistoryScreen
from screens.revenue import RevenueScreen
from screens.eod_ledger import EODLedgerScreen
from screens.ledger import LedgerScreen
from screens.pos import POSScreen

from screens.user_login import UserLoginScreen
from screens.shop_qr import ShopQRScreen
from screens.pay import PayScreen


class PalacharakApp(App):
    def build(self):

        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginTypeScreen(name="login_type"))
        sm.add_widget(OwnerSetupScreen(name="owner_setup"))
        sm.add_widget(OwnerLoginScreen(name="owner_login"))
        sm.add_widget(OwnerMenuScreen(name="owner_menu"))
        sm.add_widget(UserLoginScreen(name="user_login"))

        sm.add_widget(AddShopScreen(name="add_shop"))
        sm.add_widget(DeleteShopScreen(name="delete_shop"))
        sm.add_widget(AddUserScreen(name="add_user"))
        sm.add_widget(DeleteUserScreen(name="delete_user"))
        sm.add_widget(QRScanScreen(name="qr_scan"))
        sm.add_widget(ShopQRScreen(name="shop_qr"))

        sm.add_widget(InventoryScreen(name="inventory"))
        sm.add_widget(UpdatePriceScreen(name="update_price"))
        sm.add_widget(PriceHistoryScreen(name="price_history"))
        sm.add_widget(RevenueScreen(name="revenue"))
        sm.add_widget(LedgerScreen(name="ledger"))
        sm.add_widget(EODLedgerScreen(name="eod_ledger"))
        sm.add_widget(PayScreen(name="pay"))
        sm.add_widget(POSScreen(name="pos"))

        sm.current = "login_type"
        return sm


if __name__ == "__main__":
    PalacharakApp().run()
