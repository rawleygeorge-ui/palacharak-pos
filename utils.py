from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def popup(title, msg):
    box = BoxLayout(orientation="vertical", padding=10, spacing=10)
    box.add_widget(Label(text=msg))
    btn = Button(text="OK", size_hint_y=None, height=40)
    box.add_widget(btn)

    p = Popup(title=title, content=box, size_hint=(0.7, 0.4), auto_dismiss=False)
    btn.bind(on_release=p.dismiss)
    p.open()
