from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from brick import Brick


Builder.load_file('layout.kv')
if platform != 'android':
    Window.size = (480, 1080)


class MyLayout(BoxLayout):
    pass


class BrickGameApp(App):
    primary_background = get_color_from_hex('#2f2922')
    secondary_background = get_color_from_hex('#494136')
    primary_accent = get_color_from_hex('#ffa333')
    secondary_accent = get_color_from_hex('#ffd199')
    font_color = get_color_from_hex('#fef3e6')
    brick = [[0,1,0],[1,1,1]]
    current_brick = None
    grid_size = [10, 20]

    def build(self):
        return MyLayout()

    def on_start(self):
        self.current_brick = Brick(brick=self.brick, grid_size=self.grid_size)
        grid = self.root.ids.game_grid
        grid.add_widget(self.current_brick)

    def control_brick(self, direction):
        self.current_brick.control(direction)


if __name__ == '__main__':
    BrickGameApp().run()
