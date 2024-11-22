from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_file('game_info.kv')

class GameInformation(Screen):

    def on_enter(self):
        self.animation_schedule =Clock.schedule_interval(self.star_pulse, 2)

    def on_leave(self):
        if hasattr(self, 'animation_schedule'):
            self.animation_schedule.cancel()

    def on_button_press(self, button_instance):
        # Switch to the game screen and intiialize the game
        if button_instance == self.ids.info_back_btn:
            self.manager.current = 'start'
            

    def star_pulse(self, dt):
        star = self.ids.star_ability
        anim = Animation(opacity = 0.3, duration = 1) + Animation(opacity = 1, duration = 1)     
        anim.start(star)