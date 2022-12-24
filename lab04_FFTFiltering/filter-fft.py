import argparse
import sys

import numpy as np

from scipy import fft
from PIL import Image


MAX_PIXEL_VALUE = 255
PIXEL_THRESHOLD = MAX_PIXEL_VALUE // 2

#  Parses command-line arguments
parser = argparse.ArgumentParser(description='fft filtering with mask image')

parser.add_argument('input_image', help='input .png image')
parser.add_argument('--output_fft_result', help='output .png file with the result of the fft application after filtering with --input_ftt_mask')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--output_fft_mask', help='output .png file to receive the fft mask of the input image')
group.add_argument('--input_fft_mask', help='input .png file to with the fft mask to apply to input image')
group.add_argument('--image_distance', help='input .png file to compute Euclidean distance and RMS to input_image')

args = parser.parse_args()

if args.input_fft_mask and not args.output_fft_result:
    print('FATAL: --input_fft_mask requires --output_fft_result', file=sys.stderr)
    sys.exit(1)
elif args.output_fft_result and not args.input_fft_mask:
    print('WARNING: --output_fft_result has no effect without --input_fft_mask', file=sys.stderr)


#  Reads input images
input_image = np.asarray(Image.open(args.input_image))
input_fft_mask = None if args.input_fft_mask is None else np.asarray(Image.open(args.input_fft_mask).convert('HSV'))
image_distance = None if args.image_distance is None else np.asarray(Image.open(args.image_distance))


#  Action - Image distance
if args.image_distance:
    if input_image.shape != image_distance.shape:
        print('FATAL: input image has not the same shape as --image_distance:',
              input_image.shape, 'vs.', image_distance.shape, file=sys.stderr)
        sys.exit(1)
    n_pixels = 1. * input_image.shape[0] * input_image.shape[1]
    distance_sq = np.sum(((input_image-image_distance)**2))
    mean_sq = distance_sq / n_pixels
    print(distance_sq ** 0.5)
    print(mean_sq ** 0.5)
    sys.exit(0)


# Action - Outputs or applies the FFT mask
max_input = np.max(input_image)
if  max_input > MAX_PIXEL_VALUE:
    print(f'FATAL: maximum pixel value on input_image must be {MAX_PIXEL_VALUE}, found: {max_input}', file=sys.stderr)
    sys.exit(0)
if len(input_image.shape)>2 and input_image.shape[2]>1:
    print('WARNING: input image will converted to grayscale for FFT operations', file=sys.stderr)
    input_image = np.mean(input_image, axis=2)

input_image_fft = input_image / MAX_PIXEL_VALUE
input_image_fft = fft.fft2(input_image_fft, norm='ortho')
input_image_fft = fft.fftshift(input_image_fft)

def save_image(image_array, image_name, max_val=255., image_type='PNG'):
    image_array = np.clip(image_array, 0., max_val)
    image_array = image_array.astype(np.uint8)
    output_image = Image.fromarray(image_array)
    output_image.save(image_name, image_type)

if args.output_fft_mask:
    output_fft_mask = input_image_fft
    output_fft_mask = np.abs(output_fft_mask)
    output_fft_mask = np.log2(output_fft_mask)
    print(output_fft_mask.shape, output_fft_mask.max(), output_fft_mask.min())
    output_fft_mask = output_fft_mask - np.min(output_fft_mask)
    output_fft_mask = output_fft_mask / np.max(output_fft_mask)
    print(output_fft_mask.shape, output_fft_mask.max(), output_fft_mask.min())
    # output_fft_mask = 1. - output_fft_mask
    output_fft_mask = output_fft_mask * MAX_PIXEL_VALUE
    print(output_fft_mask.shape, output_fft_mask.max(), output_fft_mask.min())
    output_fft_mask = np.stack([output_fft_mask] * 3)
    output_fft_mask = np.transpose(output_fft_mask, axes=(1, 2, 0,))
    save_image(output_fft_mask, args.output_fft_mask)
    sys.exit(0)

if args.input_fft_mask:
    # Creates a mask that erases values on the red values
    input_fft_mask = np.where(np.logical_and.reduce([input_fft_mask[:,:,0]<10,
                                                     input_fft_mask[:,:,0]>-10,
                                                     input_fft_mask[:,:,1]>PIXEL_THRESHOLD,
                                                     input_fft_mask[:,:,2]>PIXEL_THRESHOLD]), 0., 1.)
    debug_mask = input_fft_mask * MAX_PIXEL_VALUE
    save_image(debug_mask, 'debug.png')
    # Applies the mask to the FFT
    if input_image.shape[:2] != input_fft_mask.shape:
        print('FATAL: input image has not the same shape as --input_fft_mask:',
              input_image.shape[:2], 'vs.', input_fft_mask.shape, file=sys.stderr)
        sys.exit(1)
    output_fft_result = input_image_fft * input_fft_mask
    output_fft_result = fft.ifftshift(output_fft_result)
    output_fft_result = fft.ifft2(output_fft_result, norm='ortho')
    output_fft_result = np.real(output_fft_result)*MAX_PIXEL_VALUE
    save_image(output_fft_result, args.output_fft_result)
    sys.exit(0)
