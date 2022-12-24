import numpy as np

from lib.screen import Screen
from numpy.typing import ArrayLike

def draw_line(screen: Screen, start: int, end: int, start_depth: int, end_depth: int) -> None:

    # get image parameters
    h, w, _ = screen.canvas.shape

    x0, y0, x1, y1 = start[0], start[1], end[0], end[1]

    assert x0 >=0 and x0 < w and x1 >=0 and x1 < w and y0 >=0 and y0 < h and y1 >=0 and y1 < h
    # Computes differences
    dx = x1-x0
    dy = y1-y0
    dc = abs(dx) # delta x in book - here we are using row, col coordinates
    dr = abs(dy) # delta y in book

    # z-buffer
    # z value interpolation: we interpolate the z-values between z0 (associated with pixel x0,y0)
    # and z1 (associated with pixel x1,y1) by their reciprocals: 1/z = (1/z0)*(1-q)+(1/z1)*q
    # this ensures the depths are perspective correct
    z0 = start_depth
    z1 = end_depth
    q = 0

    if dr <= dc:
        # Line inclination is at most 1
        # Swaps points if c1<c0 and converts x,y coordinates to row,col coordinates
        # dx>=0 => x1>=x0 => c1>=x0
        r0 = h-1-y0 if dx>=0 else h-1-y1
        r1 = h-1-y1 if dx>=0 else h-1-y0
        c0 =     x0 if dx>=0 else x1
        c1 =     x1 if dx>=0 else x0
        
        z0 = z0 if dx>=0 else z1
        z1 = z1 if dx>=0 else z0
        z = z0
        # setup delta_z
        if dc!=0:
            delta_q = 1/(dc)
        else:
            delta_q = 0
            if z0>z1:
                z = z0
                q = 0
            else:
                z = z1
                q = 1
        # Implements Bresenham's midpoint algorithm for lines
        # (Klawonn. Introduction to Computer Graphics. 2nd Edition. Section 4.2, pp. 45–53)
        # ...deltas of Bressenham's algorithm
        d_horizontal = 2*dr      # delta east in book
        d_diagonal   = 2*(dr-dc) # delta northeast in book
        # ...draws line
        pixel_r = r0
        pixel_c = c0
        step_row = 1 if r1>=r0 else -1
        d = 2*dr - dc # starting D value, D_init in book
        for c in range(c0, c1+1):
            # image[pixel_r, pixel_c] = color
            # zbuffer test
            # obs: z cant be 0 - since the projection point is 0, any point with z=0 wont be mapped in the canvas
            if screen.zbuffer[pixel_r, pixel_c] < z and z!=0: 
                screen.zbuffer[pixel_r, pixel_c] = z
                # draws pixel
                # y0 is converted to image (row, col) coordinates
                screen.canvas[pixel_r, pixel_c] = screen.pen
            if d<=0:
                d +=  d_horizontal
                pixel_c += 1
            else:
                d +=  d_diagonal
                pixel_r += step_row
                pixel_c += 1
            # interpolates a new z value
            if z0!=0 and z1!=0:
                z = (1/z0)*(1-q)+(1/z1)*q
                z = 1/z
            #increment q
            q += delta_q
    else:
        # Line inclination is greater than one -- inverts the roles of row and column
        # Swaps points if y1>y0 and converts x,y coordinates to row,col coordinates
        # dy<=0 => y1<=y0 => r1>=r0
        r0 = h-1-y0 if dy<=0 else h-1-y1
        r1 = h-1-y1 if dy<=0 else h-1-y0
        c0 =     x0 if dy<=0 else x1
        c1 =     x1 if dy<=0 else x0

        z0 = z0 if dy>=0 else z1
        z1 = z1 if dy>=0 else z0
        z = z0
        # setup delta_z
        if dr!=0:
            delta_q = 1/(dr)
        else:
            delta_q = 0
            if z0>z1:
                z = z0
                q = 0
            else:
                z = z1
                q = 1
        # Implements Bresenham's midpoint algorithm for lines
        # (Klawonn. Introduction to Computer Graphics. 2nd Edition. Section 4.2, pp. 45–53)
        # ...deltas of Bressenham's algorithm - same as above, but with coordinates inverted
        d_vertical = 2*dc
        d_diagonal = 2*(dc-dr)
        pixel_r = r0
        pixel_c = c0
        step_col = 1 if c1>=c0 else -1
        d = 2*dc - dr # starting D value, D_init in book
        for r in range(r0, r1+1):
            #image[pixel_r, pixel_c] = color
            # zbuffer test
            if screen.zbuffer[pixel_r, pixel_c] < z and z!=0: 
                screen.zbuffer[pixel_r, pixel_c] = z
                # draws pixel
                # y0 is converted to image (row, col) coordinates
                screen.canvas[pixel_r, pixel_c] = screen.pen
            if (d<=0):
                d +=  d_vertical
                pixel_r += 1
            else:
                d += d_diagonal
                pixel_r += 1
                pixel_c += step_col
            # interpolates a new z value
            if z0!=0 and z1!=0:
                z = (1/z0)*(1-q)+(1/z1)*q
                z = 1/z
            #increment q
            q += delta_q
