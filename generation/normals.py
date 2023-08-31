import numpy as np
from scipy import ndimage
from matplotlib import pyplot
from PIL import Image, ImageOps, ImageEnhance
import os
import sys
import config
sys.path
sys.path.append('./nvidia')
from octahedral import *
from hash.hasher import *

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def smooth_gaussian(im:np.ndarray, sigma) -> np.ndarray:

    if sigma == 0:
        return im

    im_smooth = im.astype(float)
    kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
    kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

    im_smooth = ndimage.convolve(im_smooth, kernel_x[np.newaxis])

    im_smooth = ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

    return im_smooth


def sobel(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    gradient_x = ndimage.convolve(gradient_x, kernel)
    gradient_y = ndimage.convolve(gradient_y, kernel.T)

    return gradient_x,gradient_y


def compute_normal_map(gradient_x:np.ndarray, gradient_y:np.ndarray, intensity=1):
    width = gradient_x.shape[1]
    height = gradient_x.shape[0]
    max_x = np.max(gradient_x)
    max_y = np.max(gradient_y)

    max_value = max_x

    if max_y > max_x:
        max_value = max_y

    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    intensity = 1 / intensity

    strength = max_value / (max_value * intensity)

    normal_map[..., 0] = gradient_x / max_value
    normal_map[..., 1] = gradient_y / max_value
    normal_map[..., 2] = 1 / strength

    norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

    normal_map[..., 0] /= norm
    normal_map[..., 1] /= norm
    normal_map[..., 2] /= norm

    normal_map *= 0.5
    normal_map += 0.5

    return normal_map


def generate_normal(input_file, output_file,smoothness,intensity):
    im = pyplot.imread(input_file)

    if im.ndim == 3:
        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
        im = im_grey

    im_smooth = smooth_gaussian(im, smoothness)
    sobel_x, sobel_y = sobel(im_smooth)
    normal_map = compute_normal_map(sobel_x, sobel_y, intensity)
    pyplot.imsave(output_file,LightspeedOctahedralConverter.convert_dx_to_octahedral( (normal_map * 255).astype('uint8') ))

    im = Image.open(input_file)
    im_output = Image.open(output_file)

    if( config.alpha_as_transparency ):
        r, g, b, a = im.split()
        alpha_image = Image.new("L", im.size)
        alpha_image.putdata(a.getdata())

        coordinates = x, y = 0, 0
        alpha = alpha_image.getpixel( coordinates )
        if( alpha > 5 ):
            alpha_image = ImageOps.invert(alpha_image)
            normal_face_forward = Image.new('RGB',im.size,(127,128,0))
            normal_face_forward.putalpha(alpha_image)

            im_output = Image.alpha_composite(im_output, normal_face_forward)

    im_output.save(output_file)
