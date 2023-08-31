import numpy as np
import config
from PIL import Image, ImageOps, ImageEnhance, ImageChops

def generate_roughness(input_file, output_file,intensity):
    im = Image.open(input_file)

    if( config.alpha_as_transparency ):
        r, g, b, a = im.split()
        alpha_image = Image.new("L", im.size)
        alpha_image.putdata(a.getdata())

        
    im_a = im.convert('L')
    im_a = np.array(im_a)
    im_a = ((255-im_a-9)**1.2).astype(np.uint8)
    im_a = ((255-im_a*0.9 - 5)).astype(np.uint8)
    im_a = (im_a*0.8 + 10).astype(np.uint8)

    enhancer = ImageEnhance.Contrast( Image.fromarray(im_a) )

    factor = 2
    im_output = enhancer.enhance(factor)

    if( config.alpha_as_transparency ):
        coordinates = x, y = 0, 0
        alpha = alpha_image.getpixel( coordinates )
        if( alpha > 5 ):
            im_output = ImageChops.multiply(im_output, alpha_image)

    im_output.save(output_file)
