from kivy.uix.screenmanager import Screen


class OwnerMenuScreen(Screen):
    """
    Owner / Administrator Menu Screen
    All methods referenced in owner_menu.kv are defined here.
    """

    # -------------------------
    # SHOP MANAGEMENT
    # -------------------------
    def go_add_shop(self):
        self.manager.current = "add_shop"

    def go_delete_shop(self):
        self.manager.current = "delete_shop"

    # -------------------------
    # USER MANAGEMENT
    # -------------------------
    def go_add_user(self):
        self.manager.current = "add_user"

    def go_delete_user(self):
        self.manager.current = "delete_user"

    # -------------------------
    # BUSINESS REPORTS
    # -------------------------
    def go_inventory(self):
        self.manager.current = "inventory"

    def go_revenue(self):
        self.manager.current = "revenue"

    # -------------------------
    # UTILITIES
    # -------------------------

    def go_pay(self):
        self.manager.current = "pay_unlock"

    def go_pos(self):
        self.manager.current = "pos"

    # -------------------------
    # SESSION
    # -------------------------
    def logout(self):
        self.manager.current = "login_type"
