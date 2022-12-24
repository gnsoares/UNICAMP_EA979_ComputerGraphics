import sys
from typing import Dict
from typing import List
from typing import Tuple


MAX_SIZE = 1024
MAX_LINE_LEN = 10240 - 1  # 10240 characters minus the \0 terminator


def process(
    args: List[str]
) -> Tuple[int, int, List[Dict[str, str]], str]:

    # invalid number of args: fail
    if len(args) != 3:
        tabulation = '       '
        print('usage: python draw_2d_model.py <input.dat> <output.ppm>\n'
              f'{tabulation}interprets the drawing instructions in the input'
              f' file and renders\n{tabulation}the output in the NETPBM PPM '
              'format into output.ppm')
        sys.exit(1)

    # get file names
    input_file_name = args[1]
    output_file_name = args[2]

    # Reads input file and parses its header
    with open(input_file_name, 'rt', encoding='utf-8') as input_file:
        input_lines = input_file.readlines()

    # invalid file type: fail
    if input_lines[0] != 'EA979V4\n':
        print('input file format not recognized!', file=sys.stderr)
        sys.exit(1)

    # extract image parameters
    dimensions = input_lines[1].split()
    width = int(dimensions[0])
    height = int(dimensions[1])

    # invalid image parameters: fail
    if width <= 0 or width > MAX_SIZE or height <= 0 or height > MAX_SIZE:
        print('input file has invalid image dimensions: must be >0 and <='
              f'{MAX_SIZE}!',
              file=sys.stderr)
        sys.exit(1)

    # initialize commands list
    commands = []

    # process commands
    for i, line in enumerate(input_lines[2:], start=3):

        # line too big: fail
        if len(line) > MAX_LINE_LEN:
            print(f'line {i} : line too long!', file=sys.stderr)
            sys.exit(1)

        # Blank line - skips
        if not line.strip():
            continue

        # Comment line - skips
        if line.startswith('#'):
            continue

        # extract command and parameters
        tokens = line.strip().split()
        commands.append({
            'command': tokens[0],
            'parameters': tokens[1:],
        })

    # return processed input
    return width, height, commands, output_file_name
