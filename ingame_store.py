from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from game_screen import Background, AvoidAsteroid
from spaceship_popup import purchase_window
import json



Builder.load_file('ingame_store.kv')

background = Background
background.stary_background
background.__init__
background.scroll_textures

class GameStore(Screen):

    avoid_asteroid = AvoidAsteroid


    def load_collected_coins_from_json(self):
        try:
            with open("coins.json", "r") as json_file:
                data = json.load(json_file)
                collected_coins = data.get("collected_coins", 0)
                return collected_coins
        except FileNotFoundError:
            return 0
        
    def on_enter(self):
        # Moves background
        Clock.schedule_interval(self.ids.start_background.scroll_textures, 1/60.)
    
    def on_leave(self):
        Clock.unschedule(self.ids.start_background.scroll_textures)

    def on_confirm(self, coins_required):
        collected_coins = self.load_collected_coins_from_json()

        if collected_coins >= coins_required: 
            print("Confirmed")
        else:
            print("You have not collected enough coins!")
    
    def on_deny(instance):
        print("Denied")

    
    def spaceship_popup(self, title):
        popup = purchase_window(self,
            title=title,
            content_text="Would you like to proceed with the purchase?",
            confirm_action= self.on_confirm,
            deny_action=self.on_deny
        )
        popup.open()

    def on_button_press(self, instance):

    # Handle button events
        if instance == self.ids.store_back_btn:
            self.manager.current = 'start'
        # Display the purchase window for the Scout Spaceship
        elif instance == self.ids.common_spaceship:
            self.spaceship_popup("Scout Spaceship")
            
           
        # Display the purchase window for the Torpedo Spaceship
        elif instance == self.ids.common_spaceship_1:
            self.spaceship_popup("Torpedo Spaceship")
            
        # Display the purchase window for the Fighter Spacehip
        elif instance == self.ids.uncommon_spaceship:
            self.spaceship_popup("Fighter Spaceship")
          
        # Display the purchase window for the Bomber Spaceship
        elif instance == self.ids.uncommon_spaceship_1:
            self.spaceship_popup("Bomber Spaceship")
           
        # Display the purchase window for the Diablo Spaceship
        elif instance == self.ids.epic_spaceship:
            self.spaceship_popup("Diablo Spaceship")
           
        # Display the purchase window for the Vangaurd Spaceship
        elif instance == self.ids.legendary_spaceship:
            self.spaceship_popup("Vangaurd Spaceship")

            


    

    
    