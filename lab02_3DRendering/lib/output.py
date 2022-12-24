import sys

from typing import TextIO
from numpy.typing import ArrayLike


MAX_VAL = 255


def put_string(output: str, output_file: TextIO) -> None:
    output = output.encode('ascii') if isinstance(output, str) else output
    written_n = output_file.write(output)
    if written_n != len(output):
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)


def write_ppm(image: ArrayLike, output_file: TextIO) -> None:
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


def save(name: str, image: ArrayLike) -> None:
    with open(name, 'wb') as output_file:
        write_ppm(image, output_file)
