from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from ..game.snake import SnakeGame
from .styles import KV

class GameWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SnakeGameApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        Builder.load_string(KV)
        return GameWindow() 