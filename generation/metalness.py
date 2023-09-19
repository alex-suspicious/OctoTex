import numpy as np
import config
from PIL import Image, ImageOps, ImageEnhance, ImageChops

def generate_metalness(input_file, output_file,intensity):
    im = Image.open(input_file)

    if( config.transparency_as_reflectivity ):
        try:
            r, g, b, a = im.split()
        except Exception as e:
            try:
                r, g, b = im.split()
                a = False
            except Exception as e:
                r = im.split()
                g = r
                b = r
                a = False

        if( a ):
            alpha_image = Image.new("L", im.size)
            alpha_image.putdata(a.getdata())

    im = im.convert('L')
    im_a = np.array(im)
    im_a = ((255-im_a-9)**1.15).astype(np.uint8)
    im_a = ((255-im_a*0.9 - 4)).astype(np.uint8)
    im_a = (im_a*0.35).astype(np.uint8)

    enhancer = ImageEnhance.Contrast( Image.fromarray(im_a) )

    factor = 0.8
    im_output = enhancer.enhance(factor)

    if( config.transparency_as_reflectivity and a ):
        coordinates = x, y = 0, 0
        alpha = alpha_image.getpixel( coordinates )
        if( alpha > 2 ):
            alpha_image = ImageOps.invert(alpha_image)
            normal_face_forward = Image.new('RGBA',im.size,(255,255,255,0))
            normal_face_forward.putalpha(alpha_image)

            im_output = Image.alpha_composite(im_output.convert('RGBA'), normal_face_forward)


    im_output.save(output_file)
