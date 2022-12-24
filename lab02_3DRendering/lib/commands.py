import numpy as np

from lib.objects.cube import Cube
from lib.objects.line import Line
from lib.objects.polygon import Polygon
from lib.objects.polyline import Polyline
from lib.objects.sphere import Sphere
from lib.screen import Screen
from lib.transformation import Tranformation
from typing import List


# map of object commands mnemonics to class that implements
OBJECTS = {
    'CUB': Cube,
    'L': Line,
    'P': Polyline,
    'R': Polygon,
    'SPH': Sphere,
}


def change_pen(screen: Screen,
               _: Tranformation,
               *parameters: str) -> None:
    """
    Changes pen color

    Keyword arguments:
    screen -- screen to draw into
    parameters -- list of parameters, first must be command mnemonic
    """
    screen.set_pen_color(np.array(list(map(int, parameters[1:]))))


def draw_object(screen: Screen,
                transformation: Tranformation,
                *parameters: str) -> None:
    """
    Draws object on screen

    Keyword arguments:
    screen -- screen to draw into
    transformation -- transformation object
    parameters -- list of parameters, first must be command mnemonic
    """
    object_class = OBJECTS[parameters[0]]
    object_instance = object_class(*list(map(float, parameters[1:])))
    object_instance.transform(transformation.current)
    object_instance.draw(screen)


def get_matrix_from_parameters(parameters: List[str]) -> np.ndarray:
    """
    Creates a 4x4 numpy array based on a list of parameters

    Keyword arguments:
    parameters -- list of parameters
    """
    return np.array([[
        float(parameters[4*i + j]) for j in range(4)
    ] for i in range(4)])


def multiply_transformation(_: Screen,
                            transformation: Tranformation,
                            *parameters: str) -> None:
    """
    Multiplies the current transformation matrix

    Keyword arguments:
    transformation -- transformation object
    parameters -- list of parameters, first must be command mnemonic
    """
    transformation.replace_current(
        transformation.current @ get_matrix_from_parameters(parameters[1:])
    )


def replace_transformation(_: Screen,
                           transformation: Tranformation,
                           *parameters: str) -> None:
    """
    Replaces the transformation matrix

    Keyword arguments:
    transformation -- transformation object
    parameters -- list of parameters, first must be command mnemonic
    """
    transformation.replace_current(get_matrix_from_parameters(parameters[1:]))


def replace_viewport(screen: Screen,
                     _: Tranformation,
                     *parameters: str) -> None:
    """
    Replaces the viewport projection matrix

    Keyword arguments:
    screen -- screen to draw into
    parameters -- list of parameters, first must be command mnemonic
    """
    screen.replace_viewport(get_matrix_from_parameters(parameters[1:]))

def push_transformation(_: Screen,
                           transformation: Tranformation,
                           *parameters: str) -> None:
    """
    removes last element from queue
    Keyword arguments:
    transformation -- transformation object
    parameters -- list of parameters, first must be command mnemonic
    """
    transformation.push_transformation()

def pop_transformation(_: Screen,
                           transformation: Tranformation,
                           *parameters: str) -> None:
    """
    removes last element from queue
    Keyword arguments:
    transformation -- transformation object
    parameters -- list of parameters, first must be command mnemonic
    """
    transformation.pop_transformation()

def reset(screen: Screen,
          _: Tranformation,
          *parameters: str) -> None:
    """
    Reset canvas

    Keyword arguments:
    screen -- screen to draw into
    parameters -- list of parameters, first must be command mnemonic
    """
    screen.reset(np.array(list(map(int, parameters[1:]))))
