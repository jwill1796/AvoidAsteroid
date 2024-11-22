from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.vector import Vector
from kivy.uix.widget import Widget
import random
from game_sound import GameSoundEffects

class Asteroids(Widget):

    collision = False  
    normal_ship = True
    base_speed = Window.height 
    starting_speed = base_speed *.05

    
    def __init__(self, asteroid_1, asteroid_2, asteroid_3, asteroid_4, asteroid_5, rocketship):
        super(Asteroids, self).__init__()
        
        self.asteroids = [asteroid_1, asteroid_2, asteroid_3, asteroid_4, asteroid_5]
        self.rocketship = rocketship
        self.stop_moving = False
        self.starting_speed = self.base_speed
        self.base_speed = Window.height *0.10
        self.time = 0
        self.game_time_counter = 0
        self.current_index = 0
        self.set_initial_positions()
        self.schedule_updates()

    def set_initial_positions(self):
        num_asteroids = len(self.asteroids)
        section_width = Window.width / num_asteroids

        for i, asteroid in enumerate(self.asteroids):
            asteroid.y = Window.height + 10 * (i + 1) 
            min_x = section_width * i
            max_x = section_width * (i + 1)
            asteroid.x = random.uniform(min_x, max_x )
            # Set a random fall delay for each asteroid
            asteroid.fall_delay = random.uniform(0, 5)
    
    def schedule_updates(self):
        Clock.schedule_interval(self.increment_speed, 1.0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def reset_speed(self):
        self.starting_speed = self.base_speed

    def increment_speed(self, dt):
        self.time += dt
        self.game_time_counter += dt
        if self.time >= 1:
            self.time = 0
            self.adjust_speed()
    
    def adjust_speed(self):
        if self.game_time_counter <= 90:
            self.starting_speed += 5
        elif self.game_time_counter <= 480:
            self.starting_speed += 2

    def check_for_collision(self):
        rocketship_pos = Vector(self.rocketship.pos)
        rocketship_size = Vector(self.rocketship.size)
        collided_asteroid = None # Initialize variable to hold collided asteroid
        for asteroid in self.asteroids:
            asteroid_pos = Vector(asteroid.pos)
            asteroid_size = Vector(asteroid.size)

            # Calculate the center of the rocketship and asteroid
            rocketship_center = rocketship_pos + rocketship_size / 2
            asteroid_center = asteroid_pos + asteroid_size / 2

            # Calculate the distance between the centers of the rocketship and asteroid
            distance = rocketship_center.distance(asteroid_center)

            # Calculate the sum of the radii of the rocketship and asteroid
            sum_of_radii = (rocketship_size.x + asteroid_size.x) / 2 * .68 # the larger the number the larger the hit box

            # Check for collision
            if distance < sum_of_radii and self.normal_ship :
                self.collision = True
                self.stop_moving = True
                collided_asteroid = asteroid #Store the collided asteroid 
                Clock.unschedule(self.increment_speed, self.adjust_speed)
                break
            
        return collided_asteroid # Return the collided asteroid after the loop
            
            
                
    def check_if_asteroids_reach_bottom(self, dt):
        for asteroid in self.asteroids:
            if not self.stop_moving and asteroid.y < -asteroid.height:
                self.current_index += 1
                if self.current_index == 9:
                    self.current_index = 0
                self.random_x()
            elif self.stop_moving and asteroid.y > - asteroid.height:
                asteroid.y -= self.starting_speed * dt


    def random_x(self):
        positions = [
            (Window.width * .05, Window.width * .40),
            (Window.width * .30, Window.width * .60),
            (Window.width * .55, Window.width * .85),
            (Window.width * .70, Window.width * .90),
            (Window.width * .05, Window.width * .90)  
        ]   
    
        for asteroid in self.asteroids:
            if asteroid.y < -asteroid.height:
                # Respawn the current asteroid
                index = self.asteroids.index(asteroid)
                asteroid.y = Window.height + 10 * (index + 1)
                asteroid.x = random.uniform(*positions[index])
                # Reset the fall delay for each asteroid
                asteroid.fall_delay = random.uniform(0,1)
    
    def end_movement_asteroids(self,dt):
        Clock.unschedule(self.update)

    def update(self, dt):
        for asteroid in self.asteroids:
            # Only updat the postion if the fall delay has elapsed
           asteroid.fall_delay -= dt
           if asteroid.fall_delay <= 0:
                asteroid.y -= self.starting_speed * dt
        
        collided_asteroid = self.check_for_collision()
        if collided_asteroid:
            collided_asteroid.opacity = 0

        self.check_if_asteroids_reach_bottom(dt)
