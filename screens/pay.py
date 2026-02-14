from kivy.uix.screenmanager import Screen

from utils import popup


class PayScreen(Screen):
    def pay(self):
        # Dummy payment logic (safe placeholder)
        popup("Payment Successful", "Dummy payment of ₹100 completed.")

        # Return to owner menu after payment
        self.manager.current = "owner_menu"
