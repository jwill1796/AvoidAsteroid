from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
import random
from asteroid import Asteroids

Builder.load_file('AvoidAsteroid.kv')

class StarFall(Widget):
    collected_stars = 0
    y_star = False

    def __init__(self, yellow_star, rocketship, score_board,**kwargs):
        super(StarFall, self).__init__()
        self.asteroids = Asteroids
        self.yellow_star = yellow_star
        self.timer = 0
        # This flag controls the state of the star
        self.rocketship = rocketship
        self.score_board = score_board
        self.star_falling = False
        
        
        # Start the star in a random x_pos
        self.random_x()

        # Starting position for the star
        self.yellow_star.y = Window.height + 10
        # Update the y position of the star
        Clock.schedule_interval(self.update, 1.0/60.0)

    # Detect collision of the star and rocketship
    def check_for_collision(self, dt):
        # Center of the star
        self.center_x_star = self.yellow_star.x + self.yellow_star.width / 2
        self.center_y_star = self.yellow_star.y + self.yellow_star.height / 2
        # Center of the rocketship
        self.center_x_rocket = self.rocketship.x + self.rocketship.width / 2
        self.center_y_rocket = self.rocketship.y + self.rocketship.height / 2

        distance = ((self.center_x_rocket - self.center_x_star)**2 +
                    (self.center_y_rocket - self.center_y_star)**2)**0.5
        
        distance_threshold = 50
        
        # What to do if the rocket hits the star
        if distance < distance_threshold:
            print("Immunity enabled")
            self.yellow_star.y = Window.height
            
            # Pause the star from falling
            self.star_falling = False
           
            # Allow the star to give the ship immunity to collision
            self.asteroids.normal_ship = False
            self.rocketship.opacity = .3

        if self.timer >= 10:   
            # After 10 seconds remove the ships immunity from collision
            self.asteroids.normal_ship = True
            self.rocketship.opacity = 1

        if self.timer >= 60.0:
            self.y_star = True
            self.timer = 0
            self.random_x()

    def random_x(self):
        if self.y_star:
            self.yellow_star.x = random.uniform(100, Window.width * .9)


    def update(self, dt):
        if self.star_falling:
            self.yellow_star.y -= 3
        else:  
            self.timer += dt
            
        if self.timer == 10:
            self.star_falling = True
        
        if self.yellow_star.y < -self.yellow_star.height:
            self.star_falling = False
     
        if self.timer >= 30.0:
            self.star_falling = True
            self.y_star = True
            self.timer = 0
            self.yellow_star.y = Window.height
            self.random_x()

        else:
            self.check_for_collision(dt)

        
    

