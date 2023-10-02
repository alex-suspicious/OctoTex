def list( page ):
	import requests
	from bs4 import BeautifulSoup
	import time
	from fake_useragent import UserAgent
	import json
	import os

	user_agent = UserAgent()

	directory = f"plugins/ambientcg/{page}.txt"
	isExist = os.path.exists(directory)
	if isExist:
		f = open(directory,"r")
		data = f.read()
		f.close()
		return data



	url = f"https://ambientcg.com/list?category=&type=Material&sort=Alphabet&offset={page*180}"

	re = requests.get(url, headers = { 'user-agent': user_agent.random })
	soup = BeautifulSoup(re.text,'html.parser')
	print(re.text)
	data = []
	elems = soup.find_all('img',{"class": "OnlyShowDark"})

	for elem in elems:
		# texture_url + elem = each download url
		n = elem.get('src')
		data.append(n)

	json_data = json.dumps(data)

	f = open(directory,"w")
	f.write(json_data)
	f.close()
	return json_data


def install(texture, link):
	import requests
	from bs4 import BeautifulSoup
	import time
	import shutil
	from fake_useragent import UserAgent
	import os
	import sys
	from zipfile import ZipFile, BadZipFile
	sys.path
	sys.path.append('./nvidia')
	from octahedral import LightspeedOctahedralConverter

	user_agent = UserAgent()
	directory = "plugins/ambientcg/downloads"
	isExist = os.path.exists(directory)
	if not isExist:
		os.makedirs(directory)

	isExist = os.path.exists(f"plugins/ambientcg/downloads/{link}.zip")
	if not isExist:
		r = requests.get(f"https://ambientcg.com/get?file={link}_2K-PNG.zip", headers = { 'user-agent': user_agent.random })
		with open(f"plugins/ambientcg/downloads/{link}.zip", "wb") as zipfile:
			zipfile.write(r.content)

	try:
		with ZipFile(f"plugins/ambientcg/downloads/{link}.zip", "r") as z:

			checklist = [0, 0, 0, 0]
			for file in z.namelist():
				if "Color" in file:
					checklist[0] = 1
					color_file = file

				if "NormalDX" in file:
					checklist[1] = 1
					norm_file = file

				if "Displacement" in file:
					checklist[2] = 1
					disp_file = file

				if "Roughness" in file:
					checklist[3] = 1
					rough_file = file

			if 0 not in checklist:
				z.extract(color_file, f"plugins/ambientcg/extracted/")
				z.extract(norm_file, f"plugins/ambientcg/extracted/")
				z.extract(disp_file, f"plugins/ambientcg/extracted/")
				z.extract(rough_file, f"plugins/ambientcg/extracted/")

				shutil.move(f"plugins/ambientcg/extracted/{color_file}", f"textures/processing/upscaled/{texture}.png")
				shutil.move(f"plugins/ambientcg/extracted/{norm_file}", f"textures/processing/normaldx/{texture}_normal.png")
				shutil.move(f"plugins/ambientcg/extracted/{disp_file}", f"textures/processing/displacements/{texture}_disp.png")
				shutil.move(f"plugins/ambientcg/extracted/{rough_file}", f"textures/processing/roughness/{texture}_rough.png")

				LightspeedOctahedralConverter.convert_dx_file_to_octahedral(f"textures/processing/normaldx/{texture}_normal.png", f"textures/processing/normals/{texture}_normal.png")

	except BadZipFile:
		pass