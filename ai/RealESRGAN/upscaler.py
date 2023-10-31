import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact
import gc
import config
from hash.hasher import *
from tqdm import tqdm
import shutil

def upscaleAll():
    hasherObj = hasher()
    netscale = 4
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    model_path = config.upscale_model
    denoise_strength = 0.8

    dni_weight = None
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=True,
        gpu_id=0)

    files = "textures/processing/diffuse/"
    output_dir = "textures/processing/upscaled/"

    paths = sorted(glob.glob(os.path.join(files, '*')))

    for idx, path in enumerate(paths):
        already = hasherObj.upscaled(path)
        if( already ):
            continue

        imgname, extension = os.path.splitext(os.path.basename(path))
        print(idx, imgname)

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if len(img.shape) == 3 and img.shape[2] == 4:
            img_mode = 'RGBA'
        else:
            img_mode = None

        try:
            output, _ = upsampler.enhance(img, outscale=4)
        except RuntimeError as error:
            print('Error', error)
            print('If you encounter CUDA out of memory, just moving the file...')
            shutil.move(f"textures/processing/diffuse/{imgname}.{extension}", f"textures/processing/upscaled/{imgname}.{extension}")
        except Exception as e:
            print(e)
        else:
            extension = extension[1:]
            if img_mode == 'RGBA':
                extension = 'png'

            save_path = os.path.join(output_dir, f'{imgname}.{extension}')
            cv2.imwrite(save_path, output)
            hasherObj.add_upscaled(path)

        gc.collect()

    hasherObj.saveJson()



def upscaleFile( file ):
    hasherObj = hasher()
    netscale = 4
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    model_path = config.upscale_model
    denoise_strength = 0.8

    dni_weight = None
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=True,
        gpu_id=0)

    path = "textures/processing/diffuse/" + file + ".png"
    output_dir = "textures/processing/upscaled/"

    imgname, extension = os.path.splitext(os.path.basename(path))
    #print(idx, imgname)

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if len(img.shape) == 3 and img.shape[2] == 4:
        img_mode = 'RGBA'
    else:
        img_mode = None

    try:
        output, _ = upsampler.enhance(img, outscale=4)
    except RuntimeError as error:
        print('Error', error)
        print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
    except Exception as e:
        print(e)
    else:
        extension = extension[1:]
        if img_mode == 'RGBA':
            extension = 'png'

        save_path = os.path.join(output_dir, f'{imgname}.{extension}')
        cv2.imwrite(save_path, output)

    gc.collect()

