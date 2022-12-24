import numpy as np

from lib.objects.object import Object
from lib.objects.line import Line
from lib.screen import Screen
from numpy.typing import ArrayLike

class Cube(Object):

    def __init__(self, size: str, draw_diagonals: str):
        '''
        Cube object, aggregate of lines

        Keyword arguments:
        size -- edge length
        draw_diagonals -- if true draws square diagonals on surface
        '''
        super().__init__()
        self.size = float(size)
        self.draw_diagonals = bool(draw_diagonals)

        distance: float = self.size/2 # let's do this division only one time

        self.lines: list[Line] = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    cur_coord: list = np.array([i, j, k])
                    for i2 in [-1, 1]:
                        for j2 in [-1, 1]:
                            for k2 in [-1, 1]:
                                new_coord = np.array([i2, j2, k2])
                                different_cood = int(sum(abs(new_coord - cur_coord))/2)

                                # repeated line
                                if (sum(new_coord - cur_coord) < 0):
                                    continue

                                # same coordinates
                                if (different_cood == 0):
                                    continue

                                # face diagonals
                                if (not self.draw_diagonals and different_cood == 2):
                                    continue

                                # 3d diagonals
                                if (different_cood == 3):
                                    continue
                                
                                line = Line(*(cur_coord * distance), *(new_coord * distance))
                                self.lines.append(line)
    
    def transform(self, matrix: ArrayLike) -> None:
        for line in self.lines:
            line.transform(matrix)

    def draw(self, screen: Screen) -> None:
        for line in self.lines:
            line.draw(screen)

    def __str__(self):
        return 'Cube <\n   %s\n>' % '\n   '.join(map(str, self.lines))
