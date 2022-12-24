import numpy as np

from lib.functions.draw_line import draw_line
from lib.objects.object import Object
from lib.screen import Screen
from numpy.typing import ArrayLike


class Line(Object):

    def __init__(self, *coordinates: float):
        '''
        Line object

        Keyword arguments:
        coordinates -- x and y coordinates of start and finish points of line
        '''
        super().__init__()
        self.start = np.array(coordinates[:3])
        self.end = np.array(coordinates[3:])

    def transform(self, matrix: ArrayLike) -> None:
        '''
        Applies transformation to all coordinates of object

        Keyword arguments:
        matrix -- transformation matrix
        '''
        # apply transformation in homogenous coordinates
        start_homo = matrix @ np.append(self.start, 1)
        end_homo = matrix @ np.append(self.end, 1)

        # revert coordinates to cartesian coordinates
        self.start = start_homo[:-1]/start_homo[-1]
        self.end = end_homo[:-1]/end_homo[-1]

    def clipping_code(self, point: int, xmax, ymax, xmin, ymin) -> int:
        '''
        Calculates Clipping Code for Cohen–Sutherland line clipping algorithm
        
        Keyword arguments:
        point -- 2d point 
        xmax -- right edge
        ymax -- upper edge
        xmin -- left edge
        ymin -- lower edge
        '''
        point_code = ['0','0','0','0']
        point_code[0] = '1' if point[0]<xmin else '0'
        point_code[1] = '1' if point[0]>xmax else '0'
        point_code[2] = '1' if point[1]<ymin else '0'
        point_code[3] = '1' if point[1]>ymax else '0'
        return int("".join(point_code),2)
         
    def line_clipping(self, screen: Screen, start: int, end: int) -> (int, int):
        '''
        Cohen–Sutherland line clipping algorithm

        Keyword arguments:
        screen -- screen object
        start -- line starting 2d point
        end -- line ending 2d point
        ''' 
        h, w, _ = screen.canvas.shape
        xmin = 0
        ymin = 0
        xmax = w-1# when rounded will be w-1
        ymax = h-1
        
        # clipping bit code
        p_code = self.clipping_code(start, xmax, ymax, xmin, ymin)
        q_code = self.clipping_code(end, xmax, ymax, xmin, ymin)
        x0 = start[0]
        y0 = start[1]
        x1 = end[0]
        y1 = end[1]
        
        #case 1: line inside clipping area
        if (p_code | q_code) == 0:
            return (start, end)
        #case 2: line outside clipping area
        if (p_code & q_code) != 0:
            return ((-1,-1), (-1,-1))
        #case 3: one point inside, the other outside the clipping area
        # switch if point P is inside clipping area
        if p_code == 0:
            p_code, q_code = q_code, p_code
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        # intersection with upper edge
        if (p_code & int('0001',2)) > 0 :
            x0 = x0 + (x1-x0)*(ymax-y0)/(y1-y0)
            y0 = ymax
            print("UP")
        # intersection with lower edge
        elif (p_code & int('0010',2)) > 0:
            x0 = x0 + (x1-x0)*(ymin-y0)/(y1-y0)
            y0 = ymin
            print("LOW")
        # intersection with right edge
        elif (p_code & int('0100',2)) > 0:
            y0 = y0 + (y1-y0)*(xmax-x0)/(x1-x0)
            x0 = xmax
            print("RIGHT")
        # intersection with left edge
        elif (p_code & int('1000',2)) > 0:
            y0 = y0 + (y1-y0)*(xmin-x0)/(x1-x0)
            x0 = xmin
            print("LEFT")

        # test and clip again until both points are inside the clipping area
        return self.line_clipping(screen, (x0, y0), (x1, y1)) 
    
    def draw(self, screen: Screen) -> None:
        '''
        Draws object on canvas and zbuffer

        Keyword arguments:
        screen -- screen object
        '''
        # apply projection in homogenous coordinates
        start_homo = screen.viewport @ np.append(self.start, 1)
        end_homo = screen.viewport @ np.append(self.end, 1)

        # revert coordinates to cartesian coordinates
        start_cart = start_homo[:-1]/start_homo[-1]
        end_cart = end_homo[:-1]/end_homo[-1]

        # get points in 2d
        start = start_cart[:2]
        end = end_cart[:2]

        # shift coordinates origin from center of image to upper left corner
        h, w, _ = screen.canvas.shape
        shift = np.array((w/2, h/2))
        start += shift
        end += shift
        print('points <{} -> {}>'.format(start, end))

        # line clipping
        clipped_start, clipped_end = self.line_clipping(screen, start, end)
        # line outside canvas
        if clipped_start[0]<0 or clipped_start[1]<0 or clipped_end[0]<0 or clipped_end[1]<0:
            return

        # round to pixels
        start = np.round(clipped_start).astype(np.int16)
        end = np.round(clipped_end).astype(np.int16)

        print('points <{} -> {}>'.format(start, end))
        # draw
        draw_line(screen, start, end, self.start[2], self.end[2])

    def __str__(self):
        return 'Line <{} -> {}>'.format(self.start.tolist(), self.end.tolist())
