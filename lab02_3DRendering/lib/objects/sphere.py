import math
import numpy as np

from lib.objects.object import Object
from lib.objects.line import Line
from lib.screen import Screen
from numpy.typing import ArrayLike

class Sphere(Object):

    def __init__(self,
                 radius: float,
                 num_meridians: float,
                 num_parallels: float):
        '''
        Sphere object

        Keyword arguments:
        radius -- sphere radius
        num_meridians -- quantity of meridians to draw
        num_parallels -- quantity of parallels to draw
        '''
        super().__init__()
        self.radius = radius
        self.num_meridians = int(num_meridians)
        self.num_parallels = int(num_parallels) + 2 # there are parallels on the poles
        self.lines = []

        lat: float = 0.0
        lat_increment: float = math.pi / self.num_parallels

        lng: float = 0.0
        lng_increment: float = math.pi / self.num_meridians

        for _ in range(self.num_parallels):
            for __ in range(self.num_meridians * 2):
                cur_coord = self._spherical_to_cartesian(self.radius, lat, lng)

                next_parallel = self._spherical_to_cartesian(self.radius, lat + lat_increment, lng)
                meridian_line = Line(*cur_coord, *next_parallel)
                self.lines.append(meridian_line)

                next_meridian = self._spherical_to_cartesian(self.radius, lat, lng + lng_increment)
                parallel_line = Line(*cur_coord, *next_meridian)
                self.lines.append(parallel_line)

                lng += lng_increment

            lat += lat_increment

    def _spherical_to_cartesian(self, r, theta, phi):
        '''
        Gets Cartesian (x, y, z) coordinates from spherical ones (r, theta, phi)

        Keyword arguments:
        r -- sphere radius
        theta -- parallel angle
        phi -- meridian angle
        '''
        z = r * math.sin(theta) * math.cos(phi)
        x = r * math.sin(theta) * math.sin(phi)
        y = r * math.cos(theta)
        return np.array([x, y, z])

    def transform(self, matrix: ArrayLike) -> None:
        for line in self.lines:
            line.transform(matrix)

    def draw(self, screen: Screen) -> None:
        for line in self.lines:
            line.draw(screen)

    def __str__(self):
        return 'Sphere <\n   %s\n>' % '\n   '.join(map(str, self.lines))
