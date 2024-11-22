from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.clock import Clock

class GameSoundEffects(Widget):
    def __init__(self):
        # Initialize the current sound reference to None
        self.current_sound = None
        self.ability_sound = None
        self.timer = 0
    
    def play_sound(self, sound_effect):
        # Load the sound file
        sound = SoundLoader.load(sound_effect)
        max_volume = 0.5

        def set_volume(volume):
            volume = min(volume, max_volume)
            if sound: 
                sound.volume = volume
        set_volume(0.1)
        
        # Check if the audio file is loaded correctly
        if sound:
            # If there is a currently playing sound, stop it first
            if self.current_sound and self.current_sound.state == 'play':
                self.current_sound.stop()

            # Play the new sound
            sound.play()
            
            # Store the reference to the currently playing sound
            self.current_sound = sound
        else:
            print(f"Failed to load the sound file: {sound_effect}")

    def stop_sound(self):
        # Check if there is a currently playing sound
        if self.current_sound:
            # If the current sound is playing, stop it
            if self.current_sound.state == 'play':
                self.current_sound.stop()
                print("Sound has been stopped.")
            else:
                print("No sound is currently playing.")
        else:
            print("No sound is currently loaded.")

    
    # Load the sound file that will be used upon collision of the spaceship and ability icon
    def load_sound(self, sound_filename):
        self.ability_sound = SoundLoader.load(sound_filename)
        if self.ability_sound is None:
            raise ValueError(f"Failed to load sound from file : {sound_filename}")
    
    # Play the sound when ever an ability collision occurs
    def power_up_sound(self, dt):
        if self.ability_sound is None:
            raise ValueError("Sound is not loaded. Call 'load_sound' first.")
        
        self.ability_sound.play()
        self.timer += dt

        if self.timer >= 3.0:
            self.timer = 0
            self.ability_sound.stop()
