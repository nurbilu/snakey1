from kivy.core.audio import SoundLoader
import os
import wave
import struct

class SoundManager:
    def __init__(self):
        self.eat_sound = None
        self.lose_sound = None
        self.create_default_sounds()
        self.load_sounds()

    def create_default_sounds(self):
        """Create default sound files if they don't exist"""
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        # Create ping.wav if it doesn't exist
        ping_path = os.path.join(assets_dir, 'ping.wav')
        if not os.path.exists(ping_path):
            self._create_beep_sound(ping_path, frequency=1000, duration=0.1)
        
        # Create lose.wav if it doesn't exist
        lose_path = os.path.join(assets_dir, 'lose.wav')
        if not os.path.exists(lose_path):
            self._create_beep_sound(lose_path, frequency=400, duration=0.3)

    def _create_beep_sound(self, filename, frequency=1000, duration=0.1, amplitude=0.5):
        """Create a simple beep sound file"""
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        with wave.open(filename, 'w') as wave_file:
            wave_file.setnchannels(1)  # Mono
            wave_file.setsampwidth(2)  # 2 bytes per sample
            wave_file.setframerate(sample_rate)
            
            for i in range(samples):
                value = int(32767 * amplitude * \
                          (i * frequency * 2 * 3.14159 / sample_rate))
                data = struct.pack('<h', value)
                wave_file.writeframes(data)

    def load_sounds(self):
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            self.eat_sound = SoundLoader.load(os.path.join(base_path, 'ping.wav'))
            self.lose_sound = SoundLoader.load(os.path.join(base_path, 'lose.wav'))
        except Exception as e:
            print(f"Warning: Sound files not found - {e}")

    def play_eat(self):
        if self.eat_sound:
            self.eat_sound.play()

    def play_lose(self):
        if self.lose_sound:
            self.lose_sound.play()