from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class SplashScreen(Screen):

    def on_enter(self):
        # Auto move to login screen after 1.5 seconds
        Clock.schedule_once(self.goto_login, 1.5)

    def goto_login(self, dt):
        self.manager.current = "login_type"
