from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from random import randint
from kivy.graphics import Rectangle, Color
from ..utils.sound_manager import SoundManager
from kivy.uix.floatlayout import FloatLayout

class SnakeGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = SoundManager()
        # Start snake in the middle of the playable area
        start_x = (Window.width // 2) // 20 * 20
        start_y = ((Window.height - 64) // 2) // 20 * 20
        self.snake_positions = [(start_x, start_y)]
        self.food_position = self.generate_food_position()
        self.direction = None
        self.score = 0
        self.high_score = 0
        self.game_active = False
        self.movement_speed = 0.15
        
        # Create score labels
        self.score_label = Label(
            text=f'Score: {self.score}',
            size_hint=(None, None),
            size=(140, 30),
            pos_hint={'right': 0.95, 'top': 0.95},
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        self.high_score_label = Label(
            text=f'High Score: {self.high_score}',
            size_hint=(None, None),
            size=(140, 30),
            pos_hint={'right': 0.95, 'top': 0.90},
            color=(1, 1, 1, 0.8),
            font_size='16sp'
        )
        
        # Create instruction labels
        self.instruction_label = Label(
            text='Press SPACE to Start\n\nUse Arrow Keys or WASD to move',
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            color=(1, 1, 1, 1),
            font_size='24sp',
            halign='center',
            valign='center'
        )
        
        # Create game over labels
        self.game_over_label = Label(
            text='You Lost!',
            pos_hint={'center_x': 0.5, 'center_y': 0.65},  # Adjusted position
            color=(1, 0, 0, 1),
            font_size='40sp',
            bold=True,
            halign='center',
            opacity=0
        )
        
        self.final_score_label = Label(
            text='',
            pos_hint={'center_x': 0.5, 'center_y': 0.55},  # Adjusted position
            color=(1, 1, 1, 1),
            font_size='24sp',
            halign='center',
            opacity=0
        )
        
        # Add all widgets
        self.add_widget(self.score_label)
        self.add_widget(self.high_score_label)
        self.add_widget(self.instruction_label)
        self.add_widget(self.game_over_label)
        self.add_widget(self.final_score_label)
        
        # Initialize keyboard
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def start_game(self):
        self.game_active = True
        # Start snake in the middle of the playable area
        start_x = (Window.width // 2) // 20 * 20
        start_y = ((Window.height - 64) // 2) // 20 * 20
        self.snake_positions = [(start_x, start_y)]
        self.direction = 'right'
        self.score = 0
        self.score_label.text = f'Score: {self.score}'
        self.food_position = self.generate_food_position()
        self.instruction_label.opacity = 0
        self.game_over_label.opacity = 0
        self.final_score_label.opacity = 0
        Clock.schedule_interval(self.move_snake, self.movement_speed)
        self.draw_game()

    def move_snake(self, dt):
        if not self.game_active:
            return False
        
        old_head = self.snake_positions[0]
        x, y = old_head

        # Move based on current direction
        if self.direction == 'up':
            y += 20
        elif self.direction == 'down':
            y -= 20
        elif self.direction == 'left':
            x -= 20
        elif self.direction == 'right':
            x += 20
            
        # Wrap around screen edges within playable area
        if x >= Window.width:
            x = 0
        elif x < 0:
            x = Window.width - 20
        
        if y >= Window.height - 64:  # Account for toolbar
            y = 0
        elif y < 0:
            y = Window.height - 84  # Account for toolbar
        
        new_head = (x, y)
        
        # Only check for self-collision
        if new_head in self.snake_positions:
            self.game_over()
            return False
        
        self.snake_positions.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food_position:
            self.score += 1
            self.score_label.text = f'Score: {self.score}'
            self.food_position = self.generate_food_position()
            self.sound_manager.play_eat()
        else:
            self.snake_positions.pop()
        
        self.draw_game()

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.start_game()
            return

        if not self.game_active:
            return

        # Only change direction, don't move
        if keycode[1] in ['up', 'w'] and self.direction != 'down':
            self.direction = 'up'
        elif keycode[1] in ['down', 's'] and self.direction != 'up':
            self.direction = 'down'
        elif keycode[1] in ['left', 'a'] and self.direction != 'right':
            self.direction = 'left'
        elif keycode[1] in ['right', 'd'] and self.direction != 'left':
            self.direction = 'right'

    def game_over(self):
        self.game_active = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.text = f'High Score: {self.high_score}'
        
        self.sound_manager.play_lose()
        
        # Show game over screen
        self.game_over_label.opacity = 1
        self.final_score_label.text = f'Final Score: {self.score}'
        self.final_score_label.opacity = 1
        self.instruction_label.text = 'Press SPACE to Play Again'
        self.instruction_label.opacity = 1
        
        # Stop movement clock
        Clock.unschedule(self.move_snake)
        self.draw_game()

    def draw_game(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            # Draw snake as squares
            Color(0, 0, 0)  # Black snake
            for x, y in self.snake_positions:
                Rectangle(pos=(x, y), size=(18, 18))
            
            # Draw food
            Color(1, 0, 0)  # Red food
            Rectangle(pos=self.food_position, size=(18, 18))

    def generate_food_position(self):
        # Generate food position only in playable area
        max_x = max((Window.width - 40) // 20, 1)
        max_y = max((Window.height - 104) // 20, 1)  # Adjusted for toolbar
        
        x = randint(0, max_x) * 20
        y = randint(0, max_y) * 20  # Start from bottom of playable area
        
        return (x, y)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None