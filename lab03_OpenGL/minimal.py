from __future__ import division
from __future__ import print_function

import sys

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

from PIL import Image
from PIL import ImageOps

from objects.cube import cube
from objects.sphere import sphere
from objects.spiral import spiral


def init():

    # set background color as black
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)

    # set shading model as flat (not smooth)
    gl.glShadeModel(gl.GL_FLAT)

    # red light 0
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, (5, 5, 5, 1))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, (1, 0, 0, 0.8))

    # blue light 1
    gl.glLightfv(gl.GL_LIGHT0 + 1, gl.GL_POSITION, (-5, 0, 0, 1))
    gl.glLightfv(gl.GL_LIGHT0 + 1, gl.GL_DIFFUSE, (0, 0, 1, 0.3))

    # white ambient light
    gl.glLightfv(gl.GL_LIGHT0 + 2, gl.GL_AMBIENT, (1, 1, 1, 1))

def display():

    # set the current buffers enabled for color writing
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # set opengl to render fragments only if the depth test succeeds
    gl.glEnable(gl.GL_DEPTH_TEST)

    # push current transformation matrix to stack
    gl.glPushMatrix()

    # enable lights
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glEnable(gl.GL_LIGHT0 + 1)
    gl.glEnable(gl.GL_LIGHT0 + 2)

    # material for the spheres
    mat_specular = (1,1,1,1)
    mat_shininess = 50
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mat_specular)
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, mat_shininess)

    # rotate objects
    global camera_x, camera_y
    gl.glRotatef(camera_x, 1.0, 0.0, 0.0)
    gl.glRotatef(camera_y, 0.0, 1.0, 0.0)

    # draw sphere to the left
    glut.glutSolidSphere(1.0, 20, 16)
    gl.glTranslatef(1, 0, 0)

    # draw cube at the center
    cube(2)

    # draw spiral
    gl.glTranslatef(0, 0, -3.7)
    spiral(1)
    gl.glTranslatef(0, 0, 3.7)

    # draw sphere to the right
    gl.glTranslatef(1, 0, 0)
    glut.glutSolidSphere(1.0, 20, 16)
    gl.glTranslatef(-1, 0, 0)

    # lights positions
    gl.glTranslatef(5, 0, 0)
    gl.glColor3f(1, 0, 0)
    glut.glutWireSphere(.2, 5, 5)
    gl.glTranslatef(-10, 0, 0)
    gl.glColor3f(0, 0, 1)
    glut.glutWireSphere(.2, 5, 5)
    gl.glTranslatef(5, 0, 0)

    # reset state so that other code using this get a clean state
    gl.glDisable(gl.GL_LIGHT0)
    gl.glDisable(gl.GL_LIGHT0 + 1)
    gl.glDisable(gl.GL_LIGHT0 + 2)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glDisable(gl.GL_COLOR_MATERIAL)

    # pop transformation matrix from stack
    gl.glPopMatrix()

    # disable depth checks
    gl.glDisable(gl.GL_DEPTH_TEST)

    # swap the back buffer with the front buffer
    glut.glutSwapBuffers()


def reshape(w, h):

    # define the lower left corner position of the viewport and its dimensions
    gl.glViewport(0, 0, w, h)

    # set projection perspective mode
    gl.glMatrixMode(gl.GL_PROJECTION)

    # set current transformation matrix as the identity (reset)
    gl.glLoadIdentity()

    # set the projection matrix
    glu.gluPerspective(60.0, w/h, 1.0, 20.0)

    # set model transformation (translation, rotation, scaling) mode
    gl.glMatrixMode(gl.GL_MODELVIEW)

    # set current transformation matrix as the identity (reset)
    gl.glLoadIdentity()

    # define the viewing transformation matrix
    glu.gluLookAt(5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def keyboard(key, x, y):
    global camera_x, camera_y
    if key == b's':
        camera_x = (camera_x + 10) % 360
    elif key == b'w':
        camera_x = (camera_x - 10) % 360
    elif key == b'a':
        camera_y = (camera_y + 10) % 360
    elif key == b'd':
        camera_y = (camera_y - 10) % 360
    elif key == b'c':
        render_to_jpeg()
    else:
        return
    glut.glutPostRedisplay()

# saves the viewport to an image file
def render_to_jpeg():
    x, y, width, height = gl.glGetDoublev(gl.GL_VIEWPORT)
    width, height = int(width), int(height)
    gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
    data = gl.glReadPixels(x, y, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save("out.jpeg", "JPEG")

def main():

    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(
        glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH
    )

    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(100, 100)
    glut.glutCreateWindow(sys.argv[0])

    init()

    global camera_x, camera_y
    camera_x = camera_y = 0
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()

if __name__ == "__main__":
    main()
