from kivy.core.window import Window
from kivy.uix.widget import Widget


class SpaceshipController(Widget):
    def __init__(self, spaceship):
        super(SpaceshipController, self).__init__()
        self.spaceship = spaceship
        self.initialize_spaceship()

        # getting the center of the ship
        self.center_x_ship = self.spaceship.x + self.spaceship.width / 2
        self.center_y_ship = self.spaceship.y + self.spaceship.height / 2

    def initialize_spaceship(self):
        # Set the initial position of the space ship 0.1 times the height of the window
        self.spaceship.y = Window.height * 0.25        

    def handle_touch_move(self,touch):
        # Get the size of the window
        window_width = Window.width

        # Allow the spaceship to move horiziontally
        self.spaceship.x += touch.dx

        # Constrain the spaceship within the window boundaries
        half_width = window_width * 0.99
        if self.spaceship.right >= half_width:
            self.spaceship.right = half_width
        elif self.spaceship.x < 0.05:
            self.spaceship.x = 0.05

    