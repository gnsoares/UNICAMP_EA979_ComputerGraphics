/*
 * solarsystem.c
 *
 *  Created on: 16/05/2013
 *        Author: valle
 */

#if __APPLE__
    #include <GLUT/glut.h>
    #include <OpenGL/gl.h>
    #include <OpenGL/glu.h>
#else
    #include <GL/glut.h>
    #include <GL/gl.h>
    #include <GL/glu.h>
#endif


static int year = 0, day = 0, moon1 = 0, moon2 = 0, camera = 0;

void init(void) {
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glShadeModel(GL_FLAT);
}

void display(void) {
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0, 1.0, 1.0);

    glPushMatrix();

    glRotatef((GLfloat) camera, 1.0, 0.0, 0.0);

    // draws sun
    glColor3f(1.0, 1.0, 0.0);
    glutWireSphere(1.0, 20, 16);

    // draws planet
    glRotatef((GLfloat) year, 0.0, 1.0, 0.0);
    glTranslatef(2.0, 0.0, 0.0);
    glRotatef((GLfloat) day, 0.0, 1.0, 0.0);
    glColor3f(0.0, 1.0, 1.0);
    glutWireSphere(0.2, 10, 8);
    glPushMatrix();

    // draws white moon
    glRotatef((GLfloat) moon1, 1.0, 0.0, 0.0);
    glTranslatef(0.0, 0.3, 0.0);
    glColor3f(1.0, 1.0, 1.0);
    glutWireSphere(0.05, 10, 8);
    glPopMatrix();

    // draws red moon
    glRotatef((GLfloat) moon2, 0.0, 1.0, 0.0);
    glTranslatef(0.5, 0.0, 0.0);
    glColor3f(1.0, 0.0, 0.0);
    glutWireSphere(0.07, 10, 8);

    glPopMatrix();
    glutSwapBuffers();
}

void reshape(int w, int h) {
    glViewport(0, 0, (GLsizei) w, (GLsizei) h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60.0, ((GLfloat) w)/((GLfloat) h), 1.0, 20.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
}

void keyboard(unsigned char key, int x, int y) {
    switch(key) {
    case 'c':
        camera = (camera + 10) % 360;
        glutPostRedisplay();
        break;
    case 'C':
        camera = (camera - 10) % 360;
        glutPostRedisplay();
        break;
    case 'd':
        day = (day + 10) % 360;
        glutPostRedisplay();
        break;
    case 'D':
        day = (day - 10) % 360;
        glutPostRedisplay();
        break;
    case 'm':
        moon1 = (moon1 + 10) % 360;
        glutPostRedisplay();
        break;
    case 'M':
        moon1 = (moon1 - 10) % 360;
        glutPostRedisplay();
        break;
    case 'n':
        moon2 = (moon2 + 10) % 360;
        glutPostRedisplay();
        break;
    case 'N':
        moon2 = (moon2 - 10) % 360;
        glutPostRedisplay();
        break;
    case 'y':
        year = (year + 5) % 360;
        glutPostRedisplay();
        break;
    case 'Y':
        year = (year - 5) % 360;
        glutPostRedisplay();
        break;
    default:
        break;
    }
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(500, 500);
    glutInitWindowPosition(100, 100);
    glutCreateWindow(argv[0]);
    init();
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutMainLoop();
    return 0;
}
