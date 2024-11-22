"""
Avoid Asteroid Game Module

This module contains classes representing the main game and its components.

Classes:
- Background: Represents the scrolling starry background in the game.
- AvoidAsteroid: Represents the main game screen for the Avoid Asteroid game.
"""


import os
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from ship_controller import SpaceshipController
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from asteroid import Asteroids
from star_fall import StarFall
from slowfall_settings import Slowfall
from coin_fall import coinFall
from explosion_manager import ExplosionManager
from game_sound import GameSoundEffects

Builder.load_file('AvoidAsteroid.kv')

class Background(Widget):
    """
    Background class:
    Represents the scrolling starry background in the game
    """
    stary_background = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create textures for the background
        self.stary_background = Image(source="images/SpaceBackground.png").texture
        self.stary_background.wrap = 'repeat'

        
    def scroll_textures(self, time_passed):
        """    
        Method to scroll the background textures.
        """
        scrolling_speed = Asteroids.starting_speed / 800
        # Update the uvpos of the texture for scrolling effect
        self.stary_background.uvpos = (
            self.stary_background.uvpos[0],
            (self.stary_background.uvpos[1] - time_passed * scrolling_speed) % 1
        )
        # Redraw the texture
        texture = self.property('stary_background')
        texture.dispatch(self)


class AvoidAsteroid(Screen,Background):
     """
     AvoidAsteroid class:
     Represents the main game screen for the Avoid Asteroid game.

     """
     # Load the sound effects from GameSoundEffects
     gamescreen_sound_effects = GameSoundEffects()

     def __init__(self, **kwargs):
        super(AvoidAsteroid, self).__init__(name='game')
        self.game_initialized = False
        
        # Create an instance of the GameSoundEffects class
        self.game_sound = 'audio/it_takes_a_hero.mp3'
        self.gamescreen_sound_effects = GameSoundEffects()
         
          # For scrolling background 
        Clock.schedule_interval(self.ids.background.scroll_textures, 1/60.)
 
     def initialize_game(self):
        """
        Method to initialize the game.
        """
        # Start game sound upon starting the game
        self.gamescreen_sound_effects.play_sound(self.game_sound)
        # Check if the game is already initialized
        if not self.game_initialized:
          # Reset game stats
          self.points = 0

          # initialize the spaceship_controller
          self.spaceship_controller = SpaceshipController(self.ids.spaceship)

          # Set the id for the play button
          self.play_button = self.ids.play_again
          self.play_button.opacity = 0
          self.play_button.bind(on_press=self.on_button_press)

          # Set the id for back button 
          self.back_button = self.ids.game_back_btn
          self.back_button.opacity = 0
          self.back_button.disabled = True

          # Set the game over label opacity to 0
          self.ids.game_over.opacity = 0
          
          # Save the image ID to detect collisions
          self.rocketship = self.ids["spaceship"]
          self.explosion = self.ids["explode"]
          # get the asteroid images
          self.asteroid_number_1 = self.ids["asteroid_1"]
          self.asteroid_number_2 = self.ids["asteroid_2"]
          self.asteroid_number_3 = self.ids["asteroid_3"]
          self.asteroid_number_4 = self.ids["asteroid_4"]
          self.asteroid_number_5 = self.ids["asteroid_5"]
          # get the scoreboard widget
          self.score_board = self.ids["Score"]
          # get the coins_collected widget
          self.coins_collected = self.ids["coins_collected"]
          # Set the score board text on init 
          self.score_board.text = 'Score: 0'
          # get the image of the star
          self.star = self.ids["ys"]
          # get image of the hourglass
          self.hourglass = self.ids["hg"]
          # get gif of coin
          self.coin = self.ids["coin"]
          # get game over label
          self.game_over_label = self.ids["game_over"]
          # get image of they immunity ability
          
          # Set initial opacity to 0 for images
          for image_id in ["asteroid_1", "asteroid_2", "asteroid_3", "asteroid_4", "asteroid_5",
                            "ys", "hg","explode"]:
               image = self.ids[image_id]
               image.opacity = 0

        # Start the game after 3 seconds
          self.background = self.ids.background
          Clock.schedule_once(self.start_game, 3.0)

     def start_game(self, dt):
        """
        Method to start the game.
        """
        # Create an instance of the Asteroids class 
        self.asteroids = Asteroids(self.asteroid_number_1, self.asteroid_number_2, self.asteroid_number_3,
                                    self.asteroid_number_4, self.asteroid_number_5, self.rocketship)
        # Create an instance of the Starfall class
        self.stars = StarFall(self.star, self.rocketship, self.score_board)
        # Create an instance of the Slowfall class
        self.slowfall = Slowfall(self.hourglass, self.rocketship, self.asteroids)
        # Create an instance of the coinFall calss
        self.coinfall = coinFall(self.coin, self.rocketship, self.score_board)
        # Create an instance of the Slowfall class
        self.explosion_manager = ExplosionManager(self.rocketship, self.explosion)
        # Increase the score  
        Clock.schedule_interval(self.increase_score, .5)
        # Increase the coins collected in the current game
        Clock.schedule_interval(self.increase_coins, 1.0/60.0)

        Clock.schedule_interval(self.update, 1.0/60.0)
        # Mark the game as initialized
        self.game_initialized = True
        
        # Reset the speed of the asteroids to the starting game speed
        self.asteroids.reset_speed()

        # Set opacity to 1 to make images visible
        for image_id in ["asteroid_1", "asteroid_2", "asteroid_3", "asteroid_4", "asteroid_5", "ys", "hg"]:
            image = self.ids[image_id]
            image.opacity = 1
      
     def on_touch_move(self, touch):
            """
            Method to handel touch move events.
            """
             #Call the handler method from the instantiated controller
            self.spaceship_controller.handle_touch_move(touch)
            
     def load_high_score(self):
          try:
               # Use App.user_data_dir to get the path to the app's private data directory
               file_path = os.path.join(App.get_running_app().user_data_dir, "high_score.txt")
              
               with open(file_path, "r") as file:
                    return int(file.read())
          except FileNotFoundError:
               # If the file is not found, create it and initialize high score to 0
               with open(file_path, "w") as file:
                    file.write("0")
               return 0
          except ValueError:
               # If the file is invalid, return 0 as the default high score
               return 0
     
     def update_high_score(self, new_high_score):
          try:
               # Use App.user_data_dir to get the path to the app's private data directory
               file_path = os.path.join(App.get_running_app().user_data_dir, "high_score.txt")

               # Update the new high score in the file
               with open(file_path, "w") as file:
                    file.write(str(new_high_score))
          
          except Exception as e:
               print(f" Error updating high score: {e}")
     
     def on_enter(self):
       # Schedule the animation to start after 2 seconds
          Clock.schedule_interval(self.animate_button_up_down, 2.0)

     def ui_visibility_endgame(self, dt):
         # Make the game over label visible
               self.game_over_label.color = 1,1,1,1
                # Make the play button visible
               self.play_button.opacity = 1
               # Make game over visbile
               self.game_over_label.opacity = 1
               # Make the back button visible
               self.back_button.opacity = 1
               # Enable the play button
               self.play_button.disabled = False
               self.back_button.disabled = False

     def animate_button_up_down(self, dt):
        # Access the button using the id
        play_button = self.ids.play_again
        # Define the animation
        anim = Animation(pos_hint={'center_y': 0.51}, duration=1.0) + Animation(pos_hint={'center_y': 0.49}, duration=1.0)
        # Start the animation
        anim.start(play_button)

     def on_button_press(self, instance):
               # check if this breaks game
          if instance == self.ids.play_again:
               self.game_initialized = False
               self.initialize_game()
               self.rocketship.opacity = 1
               self.explosion_manager.position_explosion()
               self.explosion.opacity = 0
               self.asteroid_number_1.source = 'images/Brown_ore1.gif'
               self.asteroid_number_2.source = 'images/Brown_ore1.gif'
               self.asteroid_number_3.source = 'images/Brown_ore1.gif'
               self.asteroid_number_4.source = 'images/Brown_ore1.gif'
               self.asteroid_number_5.source = 'images/Brown_ore1.gif'

          elif instance == self.ids.game_back_btn: 
               self.manager.current = 'start'
               self.rocketship.opacity = 1
               self.explosion_manager.position_explosion()
               self.explosion.opacity = 0
               self.asteroid_number_1.source = 'images/brown_ore1.gif'
               self.asteroid_number_2.source = 'images/brown_ore1.gif'
               self.asteroid_number_3.source = 'images/brown_ore1.gif'
               self.asteroid_number_4.source = 'images/brown_ore1.gif'
               self.asteroid_number_5.source = 'images/Brown_ore1.gif'

               self.game_initialized = False
     
     def change_image_source(self, change_asteroid, new_image_source_1):
         change_asteroid.source = new_image_source_1
    
    # Increase the score for the game
     def increase_score(self, dt):
          self.points = 10
          current_score = int(self.score_board.text.split()[-1])
          new_score = current_score + self.points
          self.score_board.text = f'Score: {new_score}'

     # Increase the amount of coins that have been collected in the current game
     def increase_coins(self, dt):
          self.current_coints = str(self.coinfall.collected_coins)
          self.coins_collected.text = f'{self.current_coints}'

     def update(self, dt):
        """
        Method to update game state.
        """
        current_score = int(self.score_board.text.split()[-1])
        score_ranges = {
               'Silver_Ore': (1000, 2000),
               'Gold_Ore': (2000, 3000),
               'Green_Ore': (3000, 4000),
               'Red_Ore': (4000, 5000),
               'Blue_Ore': (5000, 6000),
               'Purple_Ore': (6000, 7000),
               'Semi_Ore': (7000, 9000),
               'Final_Ore': (9000, 10000)
          }
        # End the game if there is a collision
        if self.asteroids.collision:
          self.game_initialized = False
          self.explosion_manager.explode()
          self.explosion_manager.position_explosion()
          self.gamescreen_sound_effects.play_sound('audio/rock_breaking.mp3')
          
          if self.game_initialized == False:
               Clock.unschedule(self.increase_score)
               Clock.unschedule(self.update)
               Clock.unschedule(self.stars.update)
               Clock.unschedule(self.slowfall.update)
               Clock.unschedule(self.coinfall.update)
               Clock.schedule_once(self.asteroids.end_movement_asteroids, 7)
               Clock.unschedule(self.asteroids.increment_speed)
               Clock.unschedule(self.asteroids.schedule_updates)
               Clock.schedule_once(self.ui_visibility_endgame, 7)
               self.asteroids.starting_speed = self.asteroids.starting_speed
               
               
               # Compare the current score with the high score
               current_score = int(self.score_board.text.split()[-1])
               high_score = self.load_high_score()

               if current_score > high_score:
                    self.update_high_score(current_score)
               
               if self.asteroids.collision == True:
                   self.back_button.disabled = False
        
          # Check each asteroid for conditions to update its image
        for ore_type, (score_min, score_max) in score_ranges.items():
               if score_min <= current_score < score_max:
                    for asteroid, asteroid_name in [(self.asteroid_number_1, "asteroid_number_1"),
                                                  (self.asteroid_number_2, "asteroid_number_2"), (self.asteroid_number_3,
                                                       "asteroid_number_3"), (self.asteroid_number_4, "asteroid_number_4"),
                                                         (self.asteroid_number_5, "asteroid_number_5")]:
                         if asteroid.y > Window.height:
                              self.change_image_source(asteroid, f'images/{ore_type}1.gif')
                              break  # Move to the next score range after updating the image of the current asteroid