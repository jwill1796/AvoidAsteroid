from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from game_screen import AvoidAsteroid
from game_screen import Background
from asteroid import Asteroids
from game_sound import GameSoundEffects


Builder.load_file('start_screen.kv')


background = Background
background.stary_background
background.__init__
background.scroll_textures


class StartScreen(Screen):
    
    avoid_asteroid = AvoidAsteroid
    asteroids = Asteroids
    startscreen_sound_effects = GameSoundEffects()
    startscreen_sound = 'audio/Space journey.mp3'
   
    def on_enter(self):
        high_score = self.avoid_asteroid.load_high_score(self)
        high_score_label = self.ids.high_score_label
        high_score_label.text = f"HIGH SCORE: {high_score}"
        # Schedule the animation to start after 2 seconds
        self.button_animation= Clock.schedule_interval(self.animate_button_up_down, 2.0)
        self.startscreen_sound_effects.play_sound(self.startscreen_sound)
        # Moves the background 
        Clock.schedule_interval(self.ids.start_background.scroll_textures, 1/60.)

    def on_leave(self):
        if hasattr(self, 'button_animation') and self.button_animation:
            self.button_animation.cancel()
        

    def animate_button_up_down(self, dt):
        
        # Access the button using the id
        start_button = self.ids.start_button
        game_info = self.ids.game_info
        sound_button_image = self.ids.sound_button
        shopping_cart = self.ids.shopping_button_background

        # Define the start button animation
        anim = Animation(pos_hint={'center_y': 0.51}, duration=1.0) + Animation(pos_hint={'center_y': 0.49}, duration=1.0)
        
        # Define the game_info button animation
        anim_1 = Animation(pos_hint={'center_y': 0.16}, duration=1.0) + Animation(pos_hint={'center_y': 0.14}, duration=1.0)
        
        # Define the sound_button animation
        anim_2 = Animation(pos_hint={'center_y': 0.16}, duration=1.0) + Animation(pos_hint={'center_y': 0.14}, duration=1.0)

        # Define the shopping button animation
        anim_3 = Animation(pos_hint={'center_y': 0.16}, duration=1.0) + Animation(pos_hint={'center_y': 0.14}, duration=1.0)

        # Start the animations
        anim.start(start_button)
        anim_1.start(game_info)
        anim_2.start(sound_button_image)
        anim_3.start(shopping_cart)

    def on_button_press(self, button_instance):
        # Switch to the game screen and intiialize the game
        if button_instance == self.ids.start_button:
            self.startscreen_sound_effects.stop_sound()
            self.manager.current = 'game'
            game_screen = self.manager.get_screen('game')
            game_screen.initialize_game()

        # Allow user to turn sound on and off in game
        if button_instance == self.ids.sound_button: # If sound is currently playing turn it off
            if self.startscreen_sound_effects.current_sound and self.startscreen_sound_effects.current_sound.state == 'play':
                self.startscreen_sound_effects.stop_sound()
                self.ids.sound_toggle.source = 'images/sound_off.png'
            
            elif self.startscreen_sound_effects.current_sound and self.startscreen_sound_effects.current_sound.state == 'stop':
                self.startscreen_sound_effects.play_sound(self.startscreen_sound)
                self.ids.sound_toggle.source = 'images/sound_on.png'
                

        # Switch to the info screen 
        elif button_instance == self.ids.game_info:
            self.manager.current = 'info'
            self.startscreen_sound_effects.stop_sound()

        elif button_instance == self.ids.shopping_button_background:
            self.manager.current = 'store'
            self.startscreen_sound_effects.stop_sound()