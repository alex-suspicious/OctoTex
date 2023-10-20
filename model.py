# That's how im running usd-core with 3.11
# Running python 3.10 with usd-core in the background...
# Someone kill me please, im begging...
import os
from tqdm import tqdm
import config
from hash.hasher import *
import platform
from usda import usda
import json

def convertUsdaTo( file, path, name ):
	#mesh_27D87220F33D10E3.usda
	f = open(file,"r")
	raw_data = f.read()
	f.close()
	data = raw_data.replace("  ","")


	newFile = "# OctoTex"

	newFile += "\n# https://github.com/alex-suspicious/OctoTex"
	newFile += f"\no {name}"

	points = data.split("point3f[] points = [")[1].split("]")[0].replace("),","\n").replace("(","v ").replace(")","").replace(" v","v").replace(",","")
	newFile += f"\n{points}"

	if( "normal3f[] normals = [" in data ):
		normals = data.split("normal3f[] normals = [")[1].split("]")[0].replace("),","\n").replace("(","vn ").replace(")","").replace(" vn","vn").replace(",","")
		newFile += f"\n{normals}"

	if( "texCoord2f[] primvars:st = [" in data ):
		uvCoords = data.split("texCoord2f[] primvars:st = [")[1].split("]")[0].replace("),","\n").replace("(","vt ").replace(")","").replace(" vt","vt").replace(",","")
		newFile += f"\n{uvCoords}"

	faces = data.split("int[] faceVertexIndices = [")[1].split("]")[0].split(", ")
	faces_data = ["f"]

	newFile += f"\ns 0"
	newFile += f"\nusemtl {name}.mtl"

	for x in range(len(faces)):
		if( (x+1)%3 == 0 ):
			if( x < len(faces)-2 ):
				faces_data.append(f" {faces[x]}/{faces[x]}\nf")
			else:
				faces_data.append(f" {faces[x]}/{faces[x]}")
		else: 
			faces_data.append(f" {faces[x]}/{faces[x]}")

	faces_data = "".join(faces_data)
	#faces_data = faces_data.replace(" /", " ")
	newFile += f"\n{faces_data}"
	newFile += "\n"
	f = open(path,"w")
	f.write(newFile)
	f.close()

	material_name = raw_data.split("def Material \"")[1].split("\"")[0]

	mtl_data = "# OctoTex MTL File: 'None'\n"
	mtl_data += "# https://github.com/alex-suspicious/OctoTex\n"
	mtl_data += "\n"
	mtl_data += f"newmtl {name}.mtl\n"
	mtl_data += "Ns 0.000000\n"
	mtl_data += "Ka 1.000000 1.000000 1.000000\n"
	mtl_data += "Ks 0.000000 0.000000 0.000000\n"
	mtl_data += "Ke 0.000000 0.000000 0.000000\n"
	mtl_data += "Ni 1.450000\n"
	mtl_data += "d 1.000000\n"
	mtl_data += "illum 1\n"
	mtl_data += f"map_Kd ../textures/processing/diffuse/{material_name.replace('mat_','')}.png"


	f = open(path.replace(".obj",".mtl"),"w")
	f.write(mtl_data)
	f.close()

	#print(data)
	#exit()

def load():
	version = platform.python_version()

	if( "3.10" not in str(version) ):
		os.system("python3.10 model.py")  
	else:
		from pxr import Usd, UsdGeom
		loadDir = "captures/meshes"

		#stage = Usd.Stage.Open(f"{config.rtx_remix_dir}/captures/capture_2023-09-15_11-28-56.usd")
		#stage.Export(f"{config.rtx_remix_dir}/captures/capture_2023-09-15_11-28-56.usda")

		hasherObj = hasher()
		dirList = os.listdir(f"{config.rtx_remix_dir}/{loadDir}/")
		success = 0

		for x in tqdm( dirList, desc="Converting..." ):
			if x.endswith(".usd"):
				#already = hasherObj.loaded(f"{config.rtx_remix_dir}/{loadDir}/{x}")
				#if( already ):
				#	continue

				try:
					stage = Usd.Stage.Open(f"{config.rtx_remix_dir}/{loadDir}/{x}")
					stage.Export(f"meshes/usda/{x.replace('usd','usda')}")

					hasherObj.add_loaded(f"{config.rtx_remix_dir}/{loadDir}/{x}")
					convertUsdaTo(f"meshes/usda/{x.replace('usd','usda')}", f"meshes/{x.replace('usd','obj')}", x.replace('.usd',''))
					success += 1
				except Exception as e:
					f = open("logs", "a")
					f.write( "\n"+str(e) )
					f.close()


		return success

if __name__ == '__main__':
	load()
