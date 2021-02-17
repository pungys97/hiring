import math


class Cabin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.middle_of_the_house = math.floor(width / 2)
        self.height_width_from_middle = math.ceil((width - 4) / 2)
        self.roof_brick = "x"
        self.wall_brick = "x"
        self.vertical_fence = "|"
        self.horizontal_fence = "="
        self.space = " "
        self.newline = "\n"
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
        return base

    def build(self):
        return self._build_roof() + self._build_base()
