# Renders a 3D model into a PPM image
import sys

from lib.commands import change_pen
from lib.commands import draw_object
from lib.commands import multiply_transformation
from lib.commands import replace_transformation
from lib.commands import push_transformation
from lib.commands import pop_transformation
from lib.commands import replace_viewport
from lib.commands import reset
from lib.input import process
from lib.screen import Screen
from lib.output import save
from lib.transformation import Tranformation


# ---------- Configuration types and constants ----------

# map of commands mnemonics to method that executes
COMMANDS = {
    'c': reset,
    'C': change_pen,
    'CUB': draw_object,
    'L': draw_object,
    'm': multiply_transformation,
    'M': replace_transformation,
    'P': draw_object,
    'POP': pop_transformation,
    'PUSH': push_transformation,
    'R': draw_object,
    'SPH': draw_object,
    'V': replace_viewport,
}


# ---------- Main routine ----------

if __name__ == '__main__':

    # process input
    width, height, commands, output = process(sys.argv)

    # initialize screen
    screen = Screen(width, height)

    # initialize transformation
    transformation = Tranformation()

    # execute all commands
    for command in commands:
        COMMANDS[command['command']](
            screen,
            transformation,
            *[command['command'], *command['parameters']]
        )

    # save file
    save(output, screen.canvas)
