from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.app import App
import random
from asteroid import Asteroids
from game_sound import GameSoundEffects
import json


class coinFall(Widget):
    y_coin = False

    def __init__(self, coin_fall, rocketship, score_board,**kkwargs):
        super(coinFall, self).__init__()
        self.sound_effects = GameSoundEffects()
        self.sound_effects.load_sound('audio/coin.mp3')
        self.asteroids = Asteroids
        self.coin_fall = coin_fall
        self.timer = 0
        self.collected_coins = 0
        # This flag controls the state of the coin
        self.rocketship = rocketship
        self.score_board = score_board
        self.coin_falling = False
        
        
        # coint the coin in a random x_pos
        self.random_x()

        # starting position for the coin
        self.coin_fall.y = Window.height + 10
        # Update the y position of the coin
        Clock.schedule_interval(self.update, 1.0/60.0)

    def write_to_json(self):
        data = {"collected_coins": self.collected_coins}

        with open("coins.json", "w") as json_file:
            json.dump(data, json_file)

    def load_from_json(self):
        try:
            with open("coins.json", "r") as json_file:
                data = json.load(json_file)
                self.collected_coins = data.get("collected_coins", 0)
        except FileNotFoundError:
            print("Your coin file was not found, is this your first game?")       

    # Detect collision of the coin and rocketship
    def check_for_collision(self, dt):
        # Center of the coin
        self.center_x_coin = self.coin_fall.x + self.coin_fall.width / 2
        self.center_y_coin = self.coin_fall.y + self.coin_fall.height / 2
        # Center of the rocketship
        self.center_x_rocket = self.rocketship.x + self.rocketship.width / 2
        self.center_y_rocket = self.rocketship.y + self.rocketship.height / 2

        distance = ((self.center_x_rocket - self.center_x_coin)**2 +
                    (self.center_y_rocket - self.center_y_coin)**2)**0.5
        
        distance_threshold = 50
        
        # What to do if the rocket hits the coin
        if distance < distance_threshold:
            print("+1 Coin")
            self.collected_coins += 1
            print(self.collected_coins)
            self.coin_fall.y = Window.height 
            # Pause the coin from falling
            self.coin_falling = False
            self.sound_effects.power_up_sound(dt)

            self.write_to_json()


        if self.timer >= 1.0:
            self.y_coin = True
            self.timer = 0
            self.random_x()

    def random_x(self):
        if self.y_coin:
            self.coin_fall.x = random.uniform(90, Window.width* .9)

    def update(self, dt):
        if self.coin_falling:
            self.coin_fall.y -= 3
        else:  
            self.timer += dt
            
        if self.timer == 1:
            self.coin_falling = True
        
        if self.coin_fall.y < -self.coin_fall.height:
            self.coin_falling = False
     
        if self.timer >= 1.0:
            self.coin_falling = True
            self.y_coin = True
            self.timer = 0
            self.coin_fall.y = Window.height
            self.random_x()

        else:
            self.check_for_collision(dt)

        
    

