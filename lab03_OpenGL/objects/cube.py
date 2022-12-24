import OpenGL.GL as gl


def cube(length: float):

    vertices = [
        (x_sign * length/2, y_sign * length/2, z_sign * length/2)
        for z_sign in (-1, 1)
        for y_sign in (-1, 1)
        for x_sign in (-1, 1)
    ]

    edge_color = (1, 1, 1)

    edges = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4),
             (0, 4), (1, 5), (3, 7), (2, 6)]

    surfaces = [(0, 1, 3, 2), (5, 4, 6, 7), (4, 0, 2, 6), (1, 5, 7, 3),
                (4, 5, 1, 0), (2, 3, 7, 6)]

    normals = [(0, 0, -1), (0, 0, 1), (-1, 0, 0), (1, 0, 0), (0, -1, 0),
               (0, 1, 0)]

    face_color = [(0.2, 0, 0.2), (0.2, 0.2, 0), (0, 0.2, 0.2), (0.2, 0, 0),
                  (0, 0.2, 0), (0, 0, 0.2)]

    # set line width
    gl.glLineWidth(3)

    # draw the edges
    gl.glColor3fv(edge_color)
    gl.glBegin(gl.GL_LINES)
    for edge in edges:
        for vertex_index in edge:
            gl.glVertex3fv(vertices[vertex_index])
    gl.glEnd()

    # reset line width
    gl.glLineWidth(1)

    # fill the faces
    gl.glBegin(gl.GL_QUADS)
    for face_index, surface in enumerate(surfaces):
        gl.glNormal3fv(normals[face_index])
        gl.glColor3fv(face_color[face_index])
        for vertex_index in surface:
            gl.glVertex3fv(vertices[vertex_index])
    gl.glEnd()
