import OpenGL.GL as gl
import math
import numpy as np

def _calcCoordinates(a, t, theta):
    x = a * t * math.cos(theta)
    y = a * t * math.sin(theta)
    return (x, y, t)
    

def spiral(size=2, height=3, itt=100):
    '''
    Create a spiral with specified size and width

    :param: size - drill width
    :param: height
    :param: itt - number of itteractions
    '''

    s = size/height
    vertices_per_cicle = int(2*math.pi//(10*height/itt))

    # Vertices list separated in 3 lists to make the drill spiral bevel
    vertices = [[], [], []]
    surfaces = []

    # Creating edges
    for t in range(itt+1):
        z = t*height/itt
        vertices[0].append(_calcCoordinates(s, z, z*10))
        vertices[1].append(_calcCoordinates(s*0.9, z+2*height/itt, z*10))
        vertices[2].append(_calcCoordinates(s, z+4*height/itt, z*10))
            
    # Drawing the base circle
    angle = 0
    while angle < 2*math.pi:
        vertices[0].append(_calcCoordinates(s, height, height*10+angle))
        angle += height/itt
    vertices[0].append(_calcCoordinates(s, height, height*10))

    # Creating surfaces - tip of the drill
    for i in range(1, vertices_per_cicle+1):
        surfaces.append((vertices[0][0], vertices[0][1], vertices[0][i], vertices[0][i-1]))
    
    # Creating surfaces - rest of the drill
    for i in range(1, itt+1):
        surfaces.append((vertices[0][i-1], vertices[0][i], vertices[1][i], vertices[1][i-1]))
        surfaces.append((vertices[1][i-1], vertices[1][i], vertices[2][i], vertices[2][i-1]))
        surfaces.append((vertices[2][i-1], vertices[2][i], vertices[0][i+vertices_per_cicle], vertices[0][i+vertices_per_cicle-1]))

    # Creating normals
    normals = list(map(lambda s: np.cross(np.asarray(s[1]) - np.asarray(s[0]), np.asarray(s[2]) - np.asarray(s[0])), surfaces))

    # reset line width
    gl.glLineWidth(1)

    # fill the faces
    gl.glBegin(gl.GL_QUADS)
    for i in range(len(surfaces)):
        gl.glNormal3fv(normals[i])
        gl.glColor3fv((1, 1, 1))
        for vertice in surfaces[i]:
            gl.glVertex3fv(vertice)
    gl.glEnd()
