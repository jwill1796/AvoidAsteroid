"""
File: avoid_asteroid_app.py
Author: [Joshua Williams]

Description:
This script defines the main application class for the Avoid Asteroid game using Kivy.
It imports necessary modules, sets up screen manager, and defines the main app class.

Dependencies:
- Kivy (https://kivy.org/)

Usage:
- Run this script to launch the Avoid Asteroid game.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from start_screen import StartScreen
from game_screen import AvoidAsteroid
from info_screen import GameInformation
from ingame_store import GameStore
# from asteroid import Asteroids


# Graphics for android
Config.set('graphics', 'width', '0') # Auto detect
Config.set('graphics', 'height', '0') # Auto detect
Config.set('graphics', 'resizable', '0') # No resize


class AvoidAsteroidApp(App):
    """
    AvoidAsteroidApp class:
    Main application class for the Avoid Asteroid game.
    """

    def build(self):    
        """
        Method to build the application UI
        """

        # Set window size
        #Window.size = (290, 400)

        # Initialize screen manager
        sm = ScreenManager()

        # Create an instance of screens
        start_screen = StartScreen(name='start')
        game_screen = AvoidAsteroid(name='game')
        info_screen = GameInformation(name='info')
        ingame_store = GameStore(name='store')

        # Add screens to screen manager
        sm.add_widget(start_screen)
        sm.add_widget(game_screen)
        sm.add_widget(info_screen)
        sm.add_widget(ingame_store)
        

        
        # Set the current screen to start_screen
        sm.current = 'start'

        return sm

# Main section
if __name__=='__main__':
    # Run the AvoidAsteroidApp
    AvoidAsteroidApp().run()

