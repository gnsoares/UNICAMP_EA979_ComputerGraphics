# Renders a 2D model into a PPM image
import sys
import numpy as np

from commands.draw_line import draw_line
from commands.polyline import polyline
from commands.polygon import polygon
from commands.change_color import change_color
from commands.paint_screen import paint_screen
from commands.matrix import set_matrix, multiply_matrix

# ---------- Configuration types and constants ----------

IMAGE_DTYPE = np.uint8
COORD_DTYPE = np.int64
MODEL_DTYPE = np.float64

MAX_SIZE = 1024
MAX_VAL = 255
MAX_LINE_LEN = 10240 - 1  # 10240 characters minus the \0 terminator
DEFAULT_BACKGROUND = 255
CHANNELS_N = 3
DEFAULT_COLOR = (0, 0, 0,)

# here we will register that functions that execute each command:
# each key of this dictionary will be the command (c, m, r, etc.)
# each value will the function that executes this command
COMMANDS = {
    'c': paint_screen,
    'L': draw_line,
    'C': change_color,
    'P': polyline,
    'R': polygon,
    'M': set_matrix,
    'm': multiply_matrix
}

# ---------- Output routines ----------


def validate_input(filename: str):

    # Reads input file and parses its header
    with open(input_file_name, 'rt', encoding='utf-8') as input_file:
        input_lines = input_file.readlines()

    # validate file format
    if input_lines[0] != 'EA979V3\n':
        print('input file format not recognized!', file=sys.stderr)
        sys.exit(1)

    # get image dimensions
    dimensions = input_lines[1].split()
    width = int(dimensions[0])
    height = int(dimensions[1])

    # validate image dimensions
    if width <= 0 or width > MAX_SIZE or height <= 0 or height > MAX_SIZE:
        print('input file has invalid image dimensions: must be > 0 and '
              f'<= {MAX_SIZE}!', file=sys.stderr)
        sys.exit(1)

    # initialize commands
    commands = []

    # validate each command
    for line_n, line in enumerate(input_lines[2:], start=3):

        if len(line) > MAX_LINE_LEN:
            print(f'line {line_n}: line too long!', file=sys.stderr)
            sys.exit(1)

        if not line.strip():
            # Blank line - skips
            continue

        command = line[0]
        parameters = line[1:].strip().split()

        if command == '#':
            continue

        if command not in COMMANDS:
            print(f'command {command} not implemented', file=sys.stderr)
            sys.exit(1)

        commands.append({
            'command': command,
            'parameters': parameters,
        })

    # return validated input
    return width, height, commands


def get_image(width: int, height: int, background: int = DEFAULT_BACKGROUND):

    # return image
    return np.full((height, width, 3),
                   fill_value=background,
                   dtype=IMAGE_DTYPE)


def put_string(output, output_file):
    output = output.encode('ascii') if isinstance(output, str) else output
    written_n = output_file.write(output)
    if written_n != len(output):
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)


def save_ppm(image, output_file):
    # Defines image header
    magic_number_1 = 'P'
    magic_number_2 = '6'
    width = image.shape[1]
    height = image.shape[0]
    end_of_header = '\n'

    # Writes header
    put_string(magic_number_1, output_file)
    put_string(magic_number_2, output_file)
    put_string('\n', output_file)
    put_string('%d %d\n' % (width, height), output_file)
    put_string('%d' % MAX_VAL, output_file)
    put_string(end_of_header, output_file)

    # Outputs image
    put_string(image.tobytes(), output_file)

# ---------- Drawing/model routines ----------


if __name__ == '__main__':

    # Parses and checks command-line arguments
    if len(sys.argv) != 3:
        print("usage: python draw_2d_model.py <input.dat> <output.ppm>\n"
              "interprets the drawing instructions in the input file and "
              "renders the output in the NETPBM PPM format into output.ppm")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    # validate input
    width, height, commands = validate_input(input_file_name)

    # get image
    image = get_image(width, height)

    # Variable initializations
    pen_color = np.array([0, 0, 0])
    matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)

    # execute all commands
    for command in commands:
        # execute command
        image, matrix = COMMANDS[command['command']](image,
                                                     pen_color,
                                                     matrix,
                                                     *command['parameters'])

    # outputs rendered image file
    with open(output_file_name, 'wb') as output_file:
        save_ppm(image, output_file)
