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

#include <math.h>
#include <stdbool.h>

static GLfloat shellA  = 0.2f;
static GLfloat shellB  = 0.2f;
static GLfloat shellC  = 0.2f;
static GLfloat shellR  = 0.1f;

static int shellStepsT = 16;
static int shellStepsS = 16;
static int cameraX = 0;
static int cameraY = 0;
static int cameraZ = 0;

static bool flat = true;
static bool normals = true;


// Polar parametric model of ellipse
// Returns distance for angle s and semi-axis a and b
GLfloat circle(
        const GLfloat s,
        const GLfloat r) {
    return sqrtf(powf(cosf(s)*r, 2.0f) + powf(sinf(s)*r, 2.0f));
}

// Parametric model of shell
//
// Source at https://www.maa.org/sites/default/files/images/upload_library/23/picado/seashells/modeloeng.html
//
// theta : parameter of surface, angle of spiral [0, final angle]
// s      : parameter of surface, angle of cross-ellipse [0, 2pi]
//
// A : spiral apperture (distance to origin at theta == 0)
// alpha : equiangular angle of generating spiral
// beta : angle between Z-axis and line from aperture local origin to XYZ origin
//
// x : float[4] vector to receive the computed coordinates X, Y, Z, W of the position
// n : float[4] vector to receive the computed coordinates X, Y, Z, W of the normal vector at position
void shell(
        const GLfloat theta,
        const GLfloat s,
        const GLfloat a,
        const GLfloat b,
        const GLfloat c,
        const GLfloat r,
        GLfloat *x,
        GLfloat *n) {

    // x[0] = (A*sinf(beta)*cosf(theta) + cosf(s)*cosf(theta)*ellipse(s, a, b)) * expf(theta / tanf(alpha));
    // x[1] = (A*sinf(beta)*sinf(theta) + cosf(s)*sinf(theta)*ellipse(s, a, b)) * expf(theta / tanf(alpha));
    // x[2] = (-A*cosf(beta) + sinf(s)*ellipse(s, a, b)) * expf(theta / tanf(alpha));

    // Position along Archimedean spiral
    GLfloat d = a + b*theta;
    x[0]  = d*cos(theta);
    x[1]  = d*sin(theta);
    x[2]  = c*theta;

    // Direction of the normal (coincides with the direction on the circle)
    d = circle(s, r);
    n[0] = d*cos(s)*cos(theta);
    n[1] = d*cos(s)*sin(theta);
    n[2] = -d*sin(s); // The sign is important so the front face points outwards

    // Final position
    x[0] += n[0];
    x[1] += n[1];
    x[2] += n[2];
    x[3]  = 1.0f;
}


// Create shell surface
void createParametricShell(
        const GLfloat a,
        const GLfloat b,
        const GLfloat c,
        const GLfloat r,
        const GLfloat minTheta,
        const GLfloat maxTheta,
        const int    stepsTheta,
        const int    stepsS) {

    const GLfloat TwoPi = 2.0f*acosf(-1.0f);
    const GLfloat thetaEps = (maxTheta-minTheta) / (GLfloat) stepsTheta;
    const GLfloat sEps = TwoPi / (GLfloat) stepsS;
    GLfloat x[4], n[3];

    glBegin(GL_TRIANGLE_STRIP);
    if (!normals) glNormal3f(0.0f, 0.0f, 1.0f);

    float theta = minTheta;

    // First vertex for seamless drawing
    shell(theta, TwoPi-sEps, a, b, c, r, x, n);
    if (normals) glNormal3fv(n);
    glVertex4fv(x);

    for (int stepTheta = 0;
        stepTheta < (stepsTheta - 1);
        theta += thetaEps, stepTheta++) {

        // Steps :  (0) | => (1) | => (2) |/ => (3) |/| => (4) |/|/| => (5) |/|/|/
        // We have to guarantee that we finish in a / step, since the next ring will both
        // complete that final triangle and start the next strip, so we want to have even steps
        float s = 0.0f;
        for (int stepS = 0;
            stepS < stepsS;
            s += sEps, stepS++) {

            shell(theta, s, a, b, c, r, x, n);
            if (normals) glNormal3fv(n);
            glVertex4fv(x);

            shell(theta+thetaEps, s, a, b, c, r, x, n);
            if (normals) glNormal3fv(n);
            glVertex4fv(x);
        }
    }

    // Last vertex for seamless drawing
    shell(theta, 0.0f, a, b, c, r, x, n);
    if (normals) glNormal3fv(n);
    glVertex4fv(x);

    glEnd();
}


void init(void)
{
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    glClearDepth(1.0f);

    if (flat) {
        glShadeModel(GL_FLAT);
        glDisable(GL_NORMALIZE);
        glDisable(GL_LIGHTING);
        glDisable(GL_LIGHT0);
    }
    else {
        glShadeModel(GL_SMOOTH);
        glEnable(GL_NORMALIZE);

        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);
        glEnable(GL_DEPTH_TEST);
    }
}

void display(void)
{
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Sets up the camera
    glLoadIdentity();
    gluLookAt (0.0f, 0.0f, 5.0f,  0.0f, 0.0f, 0.0f,  0.0f, 1.0f, 0.0f);

    if (!flat) {
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat[4]){5.0f, 10.0f, 5.0f, 1.0f});
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (GLfloat[4]){1.0f, 1.0f, 1.0f, 1.0f});
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat[4]){1.0f, 1.0f, 1.0f, 1.0f});
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (GLfloat[4]){0.1f, 0.1f, 0.1f, 1.0f});
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, 1);
     }

    glRotatef ((GLfloat) cameraX, 1.0f, 0.0f, 0.0f);
    glRotatef ((GLfloat) cameraY, 0.0f, 1.0f, 0.0f);
    glRotatef ((GLfloat) cameraZ, 0.0f, 0.0f, 1.0f);

    // Positions the lighting (fixed i.r.t. the world)

    if (!flat) {
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

        glMaterialfv (GL_FRONT, GL_AMBIENT,    (GLfloat[4]){1.0f, 1.0f, 0.0f, 1.0f} );
        glMaterialfv (GL_FRONT, GL_DIFFUSE,    (GLfloat[4]){1.0f, 1.0f, 0.0f, 1.0f} );
        glMaterialfv (GL_FRONT, GL_SPECULAR,  (GLfloat[4]){1.0f, 1.0f, 1.0f, 1.0f} );
        glMaterialf  (GL_FRONT, GL_SHININESS, 100.0f);

        glMaterialfv (GL_BACK, GL_AMBIENT,    (GLfloat[4]){0.0f, 0.0f, 1.0f, 1.0f} );
        glMaterialfv (GL_BACK, GL_DIFFUSE,    (GLfloat[4]){0.0f, 0.0f, 1.0f, 1.0f} );
        glMaterialfv (GL_BACK, GL_SPECULAR,  (GLfloat[4]){0.0f, 0.0f, 0.0f, 0.0f} );
        glMaterialf  (GL_BACK, GL_SHININESS, 0.0f);

    }
    else {
        glColor3f( 1.0f, 1.0f, 0.0f);
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    }

    createParametricShell(
        shellA,
        shellB,
        shellC,
        shellR,
        0.0f,
        12.0f,
        shellStepsT,
        shellStepsS);

    // glFlush();
    glutSwapBuffers();
}

void reshape (int w, int h)
{
    glViewport (0, 0, (GLsizei) w, (GLsizei) h);

    glMatrixMode (GL_PROJECTION);
    glLoadIdentity ();
    gluPerspective(60.0f, (GLfloat) w/(GLfloat) h, 1.0f, 20.0f);

    glMatrixMode(GL_MODELVIEW);

}


GLfloat min(GLfloat a, GLfloat b) {
    return (a<b) ? a : b;
}
GLfloat max(GLfloat a, GLfloat b) {
    return (a>b) ? a : b;
}

void keyboard (unsigned char key, int x, int y)
{
    switch (key) {
    case 'f':
    case 'F':
        flat = !flat;
        init();
        glutPostRedisplay();
        break;

    case 'n':
    case 'N':
        normals = !normals;
        glutPostRedisplay();
        break;


    case 'a':
        shellA = max(shellA - 0.05f, 0.0f);
        glutPostRedisplay();
        break;
    case 'A':
        shellA = min(shellA + 0.05f, 2.0f);
        glutPostRedisplay();
        break;

    case 'b':
        shellB = max(shellB - 0.05f, 0.05f);
        glutPostRedisplay();
        break;
    case 'B':
        shellB = min(shellB + 0.05f, 1.0f);
        glutPostRedisplay();
        break;

    case 'c':
        shellC = max(shellC - 0.05f, 0.05f);
        glutPostRedisplay();
        break;
    case 'C':
        shellC = min(shellC + 0.05f, 1.0f);
        glutPostRedisplay();
        break;

    case 'r':
        shellR = max(shellR - 0.05f, 0.05f);
        glutPostRedisplay();
        break;
    case 'R':
        shellR = min(shellR + 0.05f, 1.0f);
        glutPostRedisplay();
        break;

    case 't':
        shellStepsT = max(shellStepsT/2, 4);
        glutPostRedisplay();
        break;
    case 'T':
        shellStepsT = min(shellStepsT*2, 1024);
        glutPostRedisplay();
        break;

    case 's':
        shellStepsS = max(shellStepsS/2, 4);
        glutPostRedisplay();
        break;
    case 'S':
        shellStepsS = min(shellStepsS*2, 1024);
        glutPostRedisplay();
        break;

    case 'x':
        cameraX = (cameraX + 5) % 360;
        glutPostRedisplay();
        break;
    case 'X':
        cameraX = (cameraX - 5) % 360;
        glutPostRedisplay();
        break;
    case 'y':
        cameraY = (cameraY + 5) % 360;
        glutPostRedisplay();
        break;
    case 'Y':
        cameraY = (cameraY - 5) % 360;
        glutPostRedisplay();
        break;
    case 'z':
        cameraZ = (cameraZ + 5) % 360;
        glutPostRedisplay();
        break;
    case 'Z':
        cameraZ = (cameraZ - 5) % 360;
        glutPostRedisplay();
        break;
    case '0':
        cameraX = 0;
        cameraY = 0;
        cameraZ = 0;
        glutPostRedisplay();
        break;

    default:
        break;
    }
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize (500, 500);
    glutInitWindowPosition (100, 100);
    glutCreateWindow (argv[0]);
    init ();
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutMainLoop();
    return 0;
}
