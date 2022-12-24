import numpy as np

from lib.objects.object import Object
from lib.objects.line import Line
from lib.screen import Screen
from numpy.typing import ArrayLike


class Polyline(Object):

    def __init__(self, _: float, *coordinates: float):
        '''
        Polyline object

        Keyword arguments:
        coordinates -- list of coordinates
        '''
        super().__init__()
        self.lines = []
        for i in range(3, len(coordinates), 3):
            start = np.array(coordinates[i-3:i])
            end = np.array(coordinates[i:i+3])
            line = Line(*start, *end)
            self.lines.append(line)
            

    def transform(self, matrix: ArrayLike) -> None:
        for line in self.lines:
            line.transform(matrix)

    def draw(self, screen: Screen) -> None:
        for line in self.lines:
            line.draw(screen)

    def __str__(self):
        return 'Polyline <\n   %s\n>' % '\n   '.join(map(str, self.lines))
