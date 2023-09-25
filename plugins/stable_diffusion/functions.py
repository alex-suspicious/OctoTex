

def img2img( address, prompt, texture, steps, strength ):
	import base64
	import shutil
	import os
	import json
	import requests
	import io
	from PIL import Image, PngImagePlugin

	directory = "textures/stable_diffusion"
	isExist = os.path.exists(directory)
	if not isExist:
		os.makedirs(directory)

	isExist = os.path.exists(f"textures/stable_diffusion/{texture}.png")
	if not isExist:
		shutil.move(f"textures/processing/upscaled/{texture}.png", f"textures/stable_diffusion/{texture}.png")

	binary_fc = open(f"textures/stable_diffusion/{texture}.png", 'rb').read()
	encoded_string = base64.b64encode(binary_fc).decode('utf-8')

	payload = {
		"prompt": prompt,
		"steps": int(steps),
		"init_images": [encoded_string],
		"denoising_strength": float(strength)
	}
	
	response = requests.post(url=f"{address}/sdapi/v1/img2img", json=payload)
	r = response.json()

	for i in r['images']:
		image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

		png_payload = {
			"image": "data:image/png;base64," + i
		}
		response2 = requests.post(url=f'{address}/sdapi/v1/png-info', json=png_payload)

		pnginfo = PngImagePlugin.PngInfo()
		pnginfo.add_text("parameters", response2.json().get("info"))
		image.save(f"textures/processing/upscaled/{texture}.png", pnginfo=pnginfo)

	return "Done!"

def return_back( texture ):
	import shutil
	import os
	os.remove(f"textures/processing/upscaled/{texture}.png")
	shutil.move(f"textures/stable_diffusion/{texture}.png", f"textures/processing/upscaled/{texture}.png")
	return "Done!"