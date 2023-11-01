import os.path as osp
import glob
import cv2
import numpy as np
import torch
import ai.ESRGAN.RRDBNet_arch as arch
import gc
import config
from hash.hasher import *
from tqdm import tqdm


def upscaleAll():
    hasherObj = hasher()
    model_path = config.upscale_model
    device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
    # device = torch.device('cpu')

    test_img_folder = "textures/processing/diffuse/*"

    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=False)
    model.eval()
    model = model.to(device)

    print("Model path {:s}. \nTesting...".format(model_path))

    idx = 0
    for path in glob.glob(test_img_folder):
        already = hasherObj.upscaled(path)
        if( already ):
            continue

        idx += 1
        base = osp.splitext(osp.basename(path))[0]
        print(idx, base)
        # read images
        img = cv2.imread(path.replace("..","."), cv2.IMREAD_COLOR)
        height, width, channels = img.shape
        if( height > 2047 and width > 1023 ):
            cv2.imwrite("textures/processing/upscaled/{:s}.png".format(base).replace("..","."), img)
            continue

        img = img * 1.0 / 255
        img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
        img_LR = img.unsqueeze(0)
        img_LR = img_LR.to(device)

        with torch.no_grad():
            output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round()
        cv2.imwrite("textures/processing/upscaled/{:s}.png".format(base).replace("..","."), output)
        hasherObj.add_upscaled(path.replace("..","."))
        gc.collect()

    hasherObj.saveJson()

def upscaleFile( name ):
    hasherObj = hasher()
    model_path = config.upscale_model
    device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
    # device = torch.device('cpu')

    path = "textures/processing/diffuse/" + name + ".png"

    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=False)
    model.eval()
    model = model.to(device)

    print("Model path {:s}. \nTesting...".format(model_path))

    idx = 0
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)
    # read images
    img = cv2.imread(path.replace("..","."), cv2.IMREAD_COLOR)
    height, width, channels = img.shape
    if( height > 2047 and width > 1023 ):
        cv2.imwrite("textures/processing/upscaled/{:s}.png".format(base), img)
        return

    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite("textures/processing/upscaled/{:s}.png".format(base), output)
    gc.collect()
