from kivy.uix.popup import Popup
from kivy.metrics import dp 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image



    
def purchase_window(self, title, content_text, confirm_action, deny_action ):
    
    content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    # Lable for the window
    label = Label(text=content_text)
    label.size_hint = (1, 1)
    label.text_size = (content_layout.width, None)
    label.font_name = "fonts/PixelSans.ttf"
    label.font_size = dp(30)

    content_layout.add_widget(label)

    # Button layout
    button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
    button_layout.padding = (dp(5), 0, dp(5), 0)

    # Create confirm_button and add it to Button layout
    confirm_button = Button(size_hint=(0.3, 1), )
    confirm_button.background_color=(0,1,0,1)
    confirm_button.text=("YES")
    confirm_button.font_name = "fonts/PixelSans.ttf"
    confirm_button.font_size = dp(40)
    confirm_button.bind(on_release=confirm_action)
    button_layout.add_widget(confirm_button)

    # Create deny_button and add it to Button layout
    deny_button = Button(size_hint=(0.3, 1))
    deny_button.background_color=(1,0,0,1)
    deny_button.text=("NO")
    deny_button.font_name = "fonts/PixelSans.ttf"
    deny_button.font_size = dp(40)
    deny_button.bind(on_release=deny_action)
    button_layout.add_widget(deny_button)

    # Add Button layout to the content layout
    content_layout.add_widget(button_layout)

    # Create the popup with the content layout
    popup = Popup(title=title, content=content_layout, size_hint=(0.5,0.8))
    popup.background_color=(0.518, 0.518, 0.518, 1)
    popup.title_font= "fonts/PixelSans.ttf"
    popup.title_size=dp(50)

    return popup
    
    