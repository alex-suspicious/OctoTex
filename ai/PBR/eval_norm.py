import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision.utils import save_image

import os
import glob
import numpy as np
from tqdm import tqdm
from time import sleep
from PIL import Image
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#%%
PATH_CHK = "checkpoints/norm/norm_net_last.pth"
CROP = 1024

#%%
transform = transforms.Compose([
    transforms.Resize(CROP),
    transforms.CenterCrop(CROP),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)) # (input - mean) / std
    # outputs range from -1 to 1
])

transformDoNotResize = transforms.Compose([
    #transforms.Resize(CROP),
    #transforms.CenterCrop(CROP),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)) # (input - mean) / std
    # outputs range from -1 to 1
])

class TestDataset(Dataset):
    def __init__(self, img_dir, single = False):
        if( single ):
            self.file_list = glob.glob(img_dir)
            self.names = [os.path.splitext(os.path.basename(fp))[0] for fp in self.file_list]
            return

        self.file_list = glob.glob(img_dir+"/*.png")
        self.names = [os.path.splitext(os.path.basename(fp))[0] for fp in self.file_list]

    def __len__(self):
        return len(self.names)

    def __getitem__(self, i):
        img = Image.open(self.file_list[i]).convert('RGB')
        h, w = img.size

        if( w < 256 or h < 256 or w-300 > h or h-300 > w or w > 1024 or h > 1024 ):
            img = transform(img)
        else:
            img = transformDoNotResize(img)
        return img, self.names[i]

#%% test
def generateNorm(net, DIR_FROM, DIR_EVAL):
    output_normal = DIR_EVAL
    if not os.path.exists(output_normal):
        os.makedirs(output_normal)

    data_test = TestDataset(DIR_FROM)
    # print(batch_size)
    testloader = DataLoader(data_test, batch_size=1, shuffle=False)

    print("\nOutput disp files...")

    net.eval()
    with torch.no_grad():
        for idx, data in enumerate(testloader):
            img_in = data[0].to(device)
            img_out = net(img_in)
            # print(img_name)

            img_out_filename = os.path.join(output_normal, f"{data[1][0]}_normal.png")
            save_image(img_out, img_out_filename, value_range=(-1,1), normalize=True)

    print("Done!")

def generateNormSingle(net, DIR_FROM, DIR_EVAL):
    output_normal = DIR_EVAL
    if not os.path.exists(output_normal):
        os.makedirs(output_normal)

    data_test = TestDataset(DIR_FROM, True)
    # print(batch_size)
    testloader = DataLoader(data_test, batch_size=1, shuffle=False)

    print("\nOutput disp files...")

    net.eval()
    with torch.no_grad():
        for idx, data in enumerate(testloader):
            img_in = data[0].to(device)
            img_out = net(img_in)
            # print(img_name)

            img_out_filename = os.path.join(output_normal, f"{data[1][0]}_normal.png")
            save_image(img_out, img_out_filename, value_range=(-1,1), normalize=True)

    print("Done!")

if __name__ == "__main__":
    from model import Unet

    norm_net = Unet().to(device)
    checkpoint = torch.load(PATH_CHK)
    norm_net.load_state_dict(checkpoint["model"])

    generateNorm(norm_net,"textures","out")