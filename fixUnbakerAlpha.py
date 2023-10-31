import config
import os
import sys
from tqdm import tqdm
from PIL import Image, ImageEnhance

for x in tqdm( os.listdir(f"textures/processing/upscaled/"), desc="Generating..." ):
	if x.endswith(".png"):
		#LightspeedOctahedralConverter.convert_dx_file_to_octahedral(f"textures/processing/normaldx/{x}", f"textures/processing/normals/{x}")

		source_image = Image.open(f"textures/processing/baked/{x}")
		target_image = Image.open(f"textures/processing/upscaled/{x}")

		source_image = source_image.convert("RGBA")
		target_image = target_image.convert("RGBA")
		
		source_image = source_image.resize(target_image.size)

		# Extract the alpha channel from the source image
		alpha_channel = source_image.split()[3]

		# Create a new image by combining the RGB channels from the target image
		# and the extracted alpha channel from the source image
		new_image = Image.merge("RGBA", (target_image.split()[:3] + (alpha_channel,)))

		# Save the new image with the replaced alpha channel
		new_image.save(f"textures/processing/upscaled/{x}")