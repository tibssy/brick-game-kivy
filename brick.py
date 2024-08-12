from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.metrics import sp
import numpy as np




Builder.load_string('''
<Brick>
    rotation: 0
    scale_x: 1
    scale_y: 1
    canvas.before:
        # Color:
        #     rgba: 1,0,0,1
        # Rectangle:
        #     size: self.size
        #     pos: self.pos
        PushMatrix
        Rotate:
            angle: self.rotation
            origin: self.center
        Scale:
            x: self.scale_x
            y: self.scale_y
            origin: self.center
    canvas.after:
        PopMatrix
        
<Block@Widget>
    visible: False
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.1, 0.5) if self.visible else (0, 0, 0, 0)
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, -2
            spread_radius: 3, 3
            border_radius: [sp(6)] * 4
            blur_radius: sp(6)
        Color:
            rgba: app.secondary_accent if self.visible else (0, 0, 0, 0)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [sp(6)]
        Color:
            rgba: app.primary_accent if self.visible else (0, 0, 0, 0)
        RoundedRectangle:
            size: self.size[0] * 0.9, self.size[1] * 0.9
            pos: self.pos[0] + self.size[0] * 0.05, self.pos[1] + self.size[1] * 0.05
            radius: [sp(4)]
''')



class Brick(GridLayout):
    def __init__(self, brick, grid_size=(10, 20), **kwargs):
        super().__init__(**kwargs)
        self.brick = np.array(brick)
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
        return 1 / self.grid_size[0] * self.brick_size_x, 1 / self.grid_size[1] * self.brick_size_y

    def calculate_pos_hint(self):
        return {'x': self.position[0] / self.grid_size[0], 'y': self.position[1] / self.grid_size[1]}

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
            self.animate_rotation(self.rotation + 90)
            return

        self.animate_to_position(self.calculate_pos_hint())

    def move(self, dx, dy):
        self.position[0] = max(0, min(self.position[0] + dx, self.grid_size[0] - int(self.size_hint[0] * self.grid_size[0])))
        self.position[1] = max(0, min(self.position[1] + dy, self.grid_size[1] - int(self.size_hint[1] * self.grid_size[1])))

    def animate_to_position(self, position):
        animate_pos = Animation(pos_hint=position, duration=0.5, transition='out_expo')
        animate_pos.start(self)

    def animate_rotation(self, angle):
        self.swap_brick_dimensions()

        scale_x, scale_y = self.calculate_scale_factors()

        self.start_animations(angle, scale_x, scale_y)

    def swap_brick_dimensions(self):
        self.brick_size_x, self.brick_size_y = self.brick_size_y, self.brick_size_x

    def calculate_scale_factors(self):
        if self.brick.shape == (self.brick_size_y, self.brick_size_x):
            return 1, 1
        else:
            return self.brick_size_y / self.brick_size_x, self.brick_size_x / self.brick_size_y

    def start_animations(self, angle, scale_x, scale_y):
        animate_angle = Animation(rotation=angle, duration=0.5, transition='out_expo')
        animate_size = Animation(size_hint=self.calculate_size_hint(), duration=0.5, transition='out_expo')
        animate_scale = Animation(scale_x=scale_x, scale_y=scale_y, duration=0.5, transition='out_expo')

        animate_angle.start(self)
        animate_size.start(self)
        animate_scale.start(self)

