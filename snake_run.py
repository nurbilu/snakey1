from src.gui.window import SnakeGameApp
from kivy.core.window import Window
from kivy.config import Config

if __name__ == '__main__':
    # Disable window resizing
    Config.set('graphics', 'resizable', '0')
    
    # Set window size before creating the window
    Config.set('graphics', 'width', '1200')
    Config.set('graphics', 'height', '800')
    Config.write()
    
    # Set window position
    Window.left = 100
    Window.top = 100
    
    SnakeGameApp().run() 