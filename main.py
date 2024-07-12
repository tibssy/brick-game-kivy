from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_file('layout.kv')
if platform != 'android':
    Window.size = (480, 1080)



class MyLayout(BoxLayout):
    pass


class BrickGameApp(App):
    primary_color = get_color_from_hex('#b9f46c')
    secondary_color = get_color_from_hex('#dce7c7')
    secondary_background = get_color_from_hex('#c5c8ba')
    accent_color = get_color_from_hex('#E65100')


    def build(self):
        return MyLayout()


if __name__ == '__main__':
    BrickGameApp().run()
