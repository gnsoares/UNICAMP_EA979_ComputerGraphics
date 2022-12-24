# draw a color image

import math
import os
import sys

stdin = sys.stdin.fileno()
def get_byte():
    return os.read(stdin, 1)[0]

stdout = sys.stdout.fileno()
def put_byte(output):
    written_n = os.write(stdout, bytearray((output,)))
    if written_n != 1:
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)

def get_string():
    next_byte = get_byte()
    return_string = ''
    while True:
        return_string += chr(next_byte)
        if next_byte == 10:
            break
        next_byte = get_byte()
    return return_string
    # return sys.stdin.readline()

def put_string(output):
    output = output.encode('ascii')
    written_n = os.write(stdout, output)
    if written_n != len(output):
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)

if len(sys.argv) > 1:
    print('usage: python filter_pgm.py < input.pgm > output.pgm\n\n'
          '       filters a PGM image pixel by pixel', file=sys.stderr)
    sys.exit(1)

# Defines image header
magic_number = 'P5\n'
end_of_header = '\n'

# Reads input header
if get_string() != magic_number:
    print('invalid magic number on input image header', file=sys.stderr)
    sys.exit(1)
width, height = (int(f) for f in get_string().split())
max_val = int(get_string().strip())
if max_val > 255:
    print('cannot handle images with max_val > 255', file=sys.stderr)
    sys.exit(1)

# Writes output header
put_string(magic_number)
put_string('%d %d\n' % (width, height))
put_string('%d' % max_val)
put_string(end_of_header)

for row in range(height):
    for col in range(width):
        input_pixel = get_byte()
        output_pixel = input_pixel # Make transformation here
        output_pixel = min(output_pixel, max_val)
        output_pixel = max(output_pixel, 0)
        put_byte(output_pixel)
