import math
from datetime import timedelta

from .base_solver import BaseSolver
from ..generators.log_cabin_generator import Generator


class Solver(BaseSolver):
    required_params = ('width', 'height', )

    def get_score(self, duration) -> float:
        benchmark_duration = timedelta(seconds=10)
        return benchmark_duration/duration * 100

    def solve(self, solution):
        return (self._build_roof() + self._build_base()) == solution

    def __init__(self, seed, **kwargs):
        super().__init__()
        assert all([required_param in kwargs.keys() for required_param in Solver.required_params]), "Not all required arguments were filled."
        generator = Generator(seed=int(seed))
        self.width = int(kwargs.get("width")[0])
        assert self.width == generator.width, f"Width - {self.width} from the form does not correspond to generated one - {generator.width}."
        self.height = int(kwargs.get("height")[0])
        assert self.height == generator.height, f"Height - {self.height} from the form does not correspond to generated one - {generator.height}."
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
