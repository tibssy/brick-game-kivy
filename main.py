from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.metrics import sp
import numpy as np
from kivy.clock import Clock


Builder.load_file('layout.kv')
if platform != 'android':
    Window.size = (480, 1080)


class Brick(GridLayout):
    def __init__(self, brick, grid_size=(10, 20), **kwargs):
        super().__init__(**kwargs)
        self.brick = brick
        self.grid_size = grid_size
        self.brick_size_y, self.brick_size_x = self.brick.shape
        self.cols = self.brick_size_x
        self.spacing = sp(6)
        self.position = self.calculate_initial_position()
        self.size_hint = self.calculate_size_hint()
        self.pos_hint = self.calculate_pos_hint()

        self.build_brick()

    def calculate_initial_position(self):
        top_right = np.array(self.grid_size) - np.flip(self.brick.shape)
        return [int(top_right[0] // 2), int(top_right[1])]

    def calculate_size_hint(self):
        return (1 / self.grid_size[0] * self.brick_size_x,
                1 / self.grid_size[1] * self.brick_size_y)

    def calculate_pos_hint(self):
        return {'x': self.position[0] / self.grid_size[0],
                'y': self.position[1] / self.grid_size[1]}

    def build_brick(self):
        for block_value in self.brick.flatten():
            block = Factory.Block()
            block.visible = bool(block_value)
            self.add_widget(block)

    def control(self, direction):
        if direction == 'arrow_left':
            self.move(-1, 0)
        elif direction == 'arrow_right':
            self.move(1, 0)
        elif direction == 'arrow_down':
            self.move(0, -1)
        elif direction == 'arrow_up':
            self.move(0, 1)

        print(self.position)
        self.animate_to_position(self.calculate_pos_hint())

    def move(self, dx, dy):
        self.position[0] = max(0, min(self.position[0] + dx, self.grid_size[0] - int(self.size_hint[0] * self.grid_size[0])))
        self.position[1] = max(0, min(self.position[1] + dy, self.grid_size[1] - int(self.size_hint[1] * self.grid_size[1])))

    def animate_to_position(self, position):
        animate_pos = Animation(pos_hint=position, duration=0.5, transition='out_expo')
        animate_pos.start(self)


class MyLayout(BoxLayout):
    pass


class BrickGameApp(App):
    primary_background = get_color_from_hex('#2f2922')
    secondary_background = get_color_from_hex('#494136')
    primary_accent = get_color_from_hex('#ffa333')
    secondary_accent = get_color_from_hex('#ffd199')
    font_color = get_color_from_hex('#fef3e6')
    brick = np.array([[0,0,1],[1,1,1]])
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
