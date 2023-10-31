import ai.ESRGAN.upscaler
import ai.RealESRGAN.upscaler
import config
import shutil
import os
from tqdm import tqdm

def upscaleTextures():
	if( "Real" in config.upscale_model ):
		ai.RealESRGAN.upscaler.upscaleAll()
	else:
		ai.ESRGAN.upscaler.upscaleAll()

def upscaleTextures2X():
	print("Upscaling First time")

	if( "Real" in config.upscale_model ):
		ai.RealESRGAN.upscaler.upscaleAll()
	else:
		ai.ESRGAN.upscaler.upscaleAll()

	isExist = os.path.exists("textures/processing/lowres")
	if not isExist:
		os.makedirs("textures/processing/lowres")

	dirList = os.listdir("textures/processing/diffuse/")
	for x in tqdm( dirList, desc="Moving diffuse to lowres..." ):
		if x.endswith(".png"):
			shutil.move(f"textures/processing/diffuse/{x}", f"textures/processing/lowres/{x}")


	dirList = os.listdir("textures/processing/upscaled/")
	for x in tqdm( dirList, desc="Moving upscaled to diffuse..." ):
		if x.endswith(".png"):
			shutil.move(f"textures/processing/upscaled/{x}", f"textures/processing/diffuse/{x}")
	
	print("Upscaling second time")
	if( "Real" in config.upscale_model ):
		ai.RealESRGAN.upscaler.upscaleAll()
	else:
		ai.ESRGAN.upscaler.upscaleAll()

	dirList = os.listdir("textures/processing/lowres/")
	for x in tqdm( dirList, desc="Moving lowres back to diffuse..." ):
		if x.endswith(".png"):
			shutil.move(f"textures/processing/lowres/{x}", f"textures/processing/diffuse/{x}")


if __name__ == '__main__':
	upscaleTextures()