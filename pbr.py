from generation.normals import *
from generation.metalness import *
from generation.roughness import *
import config
import os
import sys
from tqdm import tqdm
from hash.hasher import *


force = 0
arg = ""

if( len(sys.argv) > 1 ):
	arg = sys.argv[1]

if( arg == "--force" ):
	force = 1


def generatePBR():
	hasherObj = hasher()
	for x in tqdm( os.listdir(f"textures/processing/upscaled/"), desc="Generating..." ):
		already = hasherObj.materialized(f"textures/processing/upscaled/{x}")
		if( already and not force ):
			continue

		if x.endswith(".png"):
			generate_normal(
				f"textures/processing/upscaled/{x}",
				f"textures/processing/normals/{x.replace('.png','_normal')}.png",0,1.5)

			generate_roughness(
				f"textures/processing/upscaled/{x}",
				f"textures/processing/roughness/{x.replace('.png','_rough')}.png",1)

			generate_metalness(
				f"textures/processing/upscaled/{x}",
				f"textures/processing/metallness/{x.replace('.png','_metal')}.png",1)

			hasherObj.add_materialized(f"textures/processing/upscaled/{x}")

	hasherObj.saveJson()

if __name__ == '__main__':
	generatePBR()