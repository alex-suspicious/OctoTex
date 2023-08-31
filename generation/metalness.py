import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def generate_metalness(input_file, output_file,intensity):
    im = Image.open(input_file).convert('L')
    im_a = np.array(im)
    im_a = ((255-im_a-9)**1.15).astype(np.uint8)
    im_a = ((255-im_a*0.9 - 4)).astype(np.uint8)
    im_a = (im_a*0.35).astype(np.uint8)

    enhancer = ImageEnhance.Contrast( Image.fromarray(im_a) )

    factor = 0.8
    im_output = enhancer.enhance(factor)

    im_output.save(output_file)