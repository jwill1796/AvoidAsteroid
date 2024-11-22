from kivy.clock import Clock

class ExplosionManager:

    def __init__(self, rocketship, explosion):
        self.rocketship = rocketship
        self.explosion = explosion

    def explode(self):
        self.rocketship.opacity = 0
        self.explosion.opacity = 1
        # Schedule explosion_ends to be called after 2 seconds
        Clock.schedule_once(self.explosion_ends, 6)

    def explosion_ends(self, dt):
        self.explosion.opacity = 0

    def position_explosion(self):
        self.explosion.center_x = self.rocketship.center_x
        self.explosion.center_y = self.rocketship.center_y