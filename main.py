from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform


Builder.load_file('layout.kv')
if platform != 'android':
    Window.size = (480, 1080)



class MyLayout(BoxLayout):
    pass


class BrickGameApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    BrickGameApp().run()
