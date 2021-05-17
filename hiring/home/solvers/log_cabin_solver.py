import math
from random import randint

from .base_solver import BaseSolver


class Solver(BaseSolver):
    required_params = ('width', 'height', )

    def get_score(self, *args, **kwargs):
        return randint(0, 100)

    def solve(self, solution):
        return (self._build_roof() + self._build_base()) == solution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert all([required_param in kwargs.keys() for required_param in Solver.required_params]), "Not all required arguments were filled."
        self.width = int(kwargs.get("width")[0])
        self.height = int(kwargs.get("height")[0])
        self.middle_of_the_house = math.floor(self.width / 2)
        self.height_width_from_middle = math.ceil((self.width - 4) / 2)
        self.roof_brick = "x"
        self.wall_brick = "x"
        self.vertical_fence = "|"
        self.horizontal_fence = "="
        self.space = " "
        self.newline = "\r\n"
        self.height_of_fence = 2

    def _build_roof(self):
        roof = ""
        for y_coordinate in range(self.height_width_from_middle):
            for x_coordinate in range(self.width):
                if (x_coordinate == self.middle_of_the_house - y_coordinate
                        or x_coordinate == self.middle_of_the_house + y_coordinate):
                    roof += self.roof_brick
                    continue
                roof += self.space
            roof += self.newline
        return roof

    def _build_base(self):
        base = ""
        for y_coordinate in range(self.height - self.height_width_from_middle):
            for x_coordinate in range(self.width):
                if ((x_coordinate == self.middle_of_the_house - self.height_width_from_middle   # left wall
                     or x_coordinate == self.middle_of_the_house + self.height_width_from_middle)   # right wall
                        or ((y_coordinate + self.height_width_from_middle + 1 == self.height
                             or y_coordinate == 0)
                            and (1 < x_coordinate < self.width - 2))):
                    base += self.wall_brick
                    continue
                if y_coordinate == self.height - self.height_of_fence - self.height_width_from_middle:     # horizontal fence
                    base += self.horizontal_fence
                    continue
                if y_coordinate > self.height - self.height_of_fence - self.height_width_from_middle and x_coordinate % 2 == 0:     # vertical fence
                    base += self.vertical_fence
                    continue
                base += self.space
            base += self.newline
        base = base[:-2]  # remove last 'newline'
        return base
