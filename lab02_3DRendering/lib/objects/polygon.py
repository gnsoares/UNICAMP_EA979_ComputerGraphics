from lib.objects.polyline import Polyline


class Polygon(Polyline):

    def __init__(self, *coordinates: str) -> None:
        '''
        Polyline object

        Keyword arguments:
        coordinates -- list of coordinates
        '''
        super().__init__(*coordinates, *coordinates[1:4])

    def __str__(self):
        return 'Polyline <\n   %s\n>' % '\n   '.join(map(str, self.lines))
