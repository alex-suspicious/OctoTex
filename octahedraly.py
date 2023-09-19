import config
import os
import sys
from tqdm import tqdm
sys.path
sys.path.append('./nvidia')
from octahedral import *

for x in tqdm( os.listdir(f"textures/processing/normaldx/"), desc="Generating..." ):
	if x.endswith(".png"):
		LightspeedOctahedralConverter.convert_dx_file_to_octahedral(f"textures/processing/normaldx/{x}", f"textures/processing/normals/{x}")