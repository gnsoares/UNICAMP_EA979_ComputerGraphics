# acabamos nao usando essa esfera na renderizacao final

import OpenGL.GL as gl
import math

def my_range(start, end, step):

    while start <= end:

        yield start
        start += step

def sphere(radius):

    for theta in my_range(0, 2*math.pi, 0.001 * math.pi):

        # Triangular mesh.

        gl.glBegin(gl.GL_TRIANGLE_STRIP)

        for phi in my_range(0, math.pi, 0.001 * math.pi):

            # Inicial point.

            x = radius * math.cos(theta) * math.sin(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(phi)
            gl.glVertex3f(x, y, z)

            # Neighboring point.

            x = radius * math.cos(theta) * math.sin(phi + 0.001 * math.pi)
            y = radius * math.sin(theta) * math.sin(phi + 0.001 * math.pi)
            z = radius * math.cos(phi + 0.001 * math.pi)
            gl.glVertex3f(x, y, z)

        gl.glEnd()
