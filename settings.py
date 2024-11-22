from kivy.core.window import Window
from kivy.event import EventDispatcher

class Settings():
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        
        self.height = Window.height
        self.width = Window.width

        Window.bind(on_resize=self.update_width)

    # Update the windows width and height when resized
    def update_width(self, instance, width, height):
        self.width = width
        self.height = height


    # Set the width of the window to 80% for other objects to use as padding
    def get_width(self):
        eighty_width = self.width * .8
        return eighty_width
    
