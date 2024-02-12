import glob
import os

import torch
from PIL import Image, ImageEnhance, ImageFilter
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.utils import save_image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# %%
PATH_CHK = "checkpoints/Roughness/latest_net_G.pth"

transformResize = transforms.Compose([
    transforms.Resize(2048),
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5)
    # outputs range from -1 to 1
])


class TestDataset(Dataset):
    def __init__(self, img_dir, single=False):
        if (single):
            self.file_list = glob.glob(img_dir)
            self.names = [os.path.splitext(os.path.basename(fp))[0] for fp in self.file_list]
            return

        self.file_list = glob.glob(img_dir + "/*.png")
        self.names = [os.path.splitext(os.path.basename(fp))[0] for fp in self.file_list]

    def __len__(self):
        return len(self.names)

    def __getitem__(self, i):
        img = Image.open(self.file_list[i]).convert('RGB')
        h, w = img.size

        img = transformResize(img)

        return img, self.names[i]


# %% test
def generateRough(net, DIR_FROM, DIR_EVAL):
    output_normal = DIR_EVAL
    if not os.path.exists(output_normal):
        os.makedirs(output_normal)

    data_test = TestDataset(DIR_FROM)
    # print(batch_size)
    testloader = DataLoader(data_test, batch_size=1, shuffle=False)

    print("\nProcessing roughness files...")

    net.eval()
    with torch.no_grad():
        for idx, data in enumerate(testloader):
            img_in = data[0].to(device).half()
            img_out = net(img_in)
            # print(img_name)

            img_out_filename = os.path.join(output_normal, f"{data[1][0]}_rough.png")
            save_image(img_out, img_out_filename, value_range=(-1, 1), normalize=True)

            im = Image.open(img_out_filename).convert("L")

            im_output = im.filter(ImageFilter.GaussianBlur(2))
            enhancer = ImageEnhance.Contrast(im_output)

            factor = 2
            im_output = enhancer.enhance(factor)
            im_output.save(img_out_filename)

    print("Done!")


def generateRoughSingle(net, DIR_FROM, DIR_EVAL):
    output_normal = DIR_EVAL
    if not os.path.exists(output_normal):
        os.makedirs(output_normal)

    data_test = TestDataset(DIR_FROM, True)
    # print(batch_size)
    testloader = DataLoader(data_test, batch_size=1, shuffle=False)

    print("\nProcessing roughness files...")

    net.eval()
    with torch.no_grad():
        for idx, data in enumerate(testloader):
            img_in = data[0].to(device)
            img_out = net(img_in)
            # print(img_name)

            img_out_filename = os.path.join(output_normal, f"{data[1][0]}_rough.png")
            save_image(img_out, img_out_filename, value_range=(-1, 1), normalize=True)

            im = Image.open(img_out_filename).convert("L")
            enhancer = ImageEnhance.Contrast(im)

            factor = 1.1
            im_output = enhancer.enhance(factor)
            im_output = im_output.filter(ImageFilter.GaussianBlur(1))
            im_output.save(img_out_filename)

    print("Done!")


if __name__ == "__main__":
    from model import OLDPBR

    # Define the model
    model = OLDPBR().cuda().half()

    # Load the trained model weights
    model.load_state_dict(torch.load('./checkpoints/Roughness/latest_net_G.pth'))

    # Set the model to evaluation mode (e.g., for batch normalization and dropout)
    model.eval()

    generateRough(model, "./textures", "./out")
