from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.app import App
from kivy.vector import Vector
import random
from asteroid import Asteroids
from star_fall import StarFall

class Slowfall(Widget):
    def __init__(self, hour_glass, rocketship, asteroids_instance):
        super(Slowfall, self).__init__()
        self.hour_glass = hour_glass
        self.rocketship = rocketship
        self.timer = 0 
        self.glass_falling = False
        self.asteroids_instance = asteroids_instance
        self.starfall = StarFall
        self.collision_cooldown = False
        self.cooldown_timer = 0
        
        # Start the hourglass at a random x pos
        self.random_x()

        # Start the hourglass at a y pos higher than the screen
        self.hour_glass.y = Window.height + 10
        
        # Update the y position of the hourglass
        Clock.schedule_interval(self.update, 0.01)

    def check_for_collision(self, dt):
        if not self.collision_cooldown:
            rocketship_pos = Vector(self.rocketship.pos)
            rocketship_size = Vector(self.rocketship.size)

            hour_glass_pos = Vector(self.hour_glass.pos)
            hour_glass_size = Vector(self.hour_glass.size)

            # Calculate the center of the rocketship and hourglass
            rocketship_center = rocketship_pos + rocketship_size / 2
            hour_glass_center = hour_glass_pos + hour_glass_size / 2

            # Calculate the distance between the centers of the rocketship and hourglass
            distance = rocketship_center.distance(hour_glass_center)
            
            # Calculate the sum of the radii of the rocketship and hourglass
            sum_of_radii = (rocketship_size.x + hour_glass_size.x) / 2

            if distance <= sum_of_radii:
                # Enable slowfall effect
                print("Slowfall enabled")
                self.glass_falling = False
                self.timer = 0
                self.hour_glass.y = Window.height + 10
                self.random_x()
                self.asteroids_instance.starting_speed = self.asteroids_instance.starting_speed / 2
                print(f"This is the current speed {self.asteroids_instance.starting_speed}")
                # Remove slowfall after 10 seconds
                Clock.unschedule(self.remove_slowfall)
                Clock.schedule_once(self.remove_slowfall, 10)  
                # Set collision cooldown
                self.collision_cooldown = True

    def remove_slowfall(self, dt):
        print("Slowfall disabled")
        self.asteroids_instance.starting_speed = self.asteroids_instance.starting_speed * 2
        # Reset collision cooldown after slowfall duration
        self.collision_cooldown = False
        

    def random_x(self):
        self.hour_glass.x = random.uniform(100, Window.width * .9)

    def update(self, dt):
        self.check_for_collision(dt)

        if self.glass_falling:
            self.hour_glass.y -= 3
        else: 
            self.timer += dt

        if self.timer >= 50:
            self.glass_falling = True
            self.timer = 0
            self.hour_glass.y = Window.height + 10
            self.random_x()

        if self.hour_glass.y < -self.hour_glass.height:
            self.glass_falling = False
            self.timer = 0
            


        

