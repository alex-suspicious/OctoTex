from PIL import Image
import os
from tqdm import tqdm
import config
from hash.hasher import *
import pathlib

loadDirId = 0
loadDir = "captures"

neededDirectories = ["textures","textures/processing","textures/processing/upscaled","textures/processing/roughness","textures/processing/normals","textures/processing/metallness","textures/processing/emission","textures/processing/diffuse"]


for directory in neededDirectories:
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)

mods = [f for f in pathlib.Path().glob("../rtx-remix/mods/*")]
if( len(mods) > 0 ):
    print("Directories for importing: ")

    print("0 | captures")
    for x in range(len(mods)):
        mod_path = str(mods[x]).replace("../rtx-remix/mods/","")
        print(f"{x+1} | {mod_path}")


    loadDirId = int(input("From what dir you want to load the textures, select by index: "))
    loadDirId -= 1
    if( loadDirId != -1 ):
        loadDir = str(mods[loadDirId]).replace("../rtx-remix/","") + "/SubUSDs/textures/diffuse"
    else:
        loadDir += "/textures"

hasherObj = hasher()
for x in tqdm( os.listdir(f"{config.rtx_remix_dir}/{loadDir}/"), desc="Converting..." ):
    if x.endswith(".dds"):
        already = hasherObj.loaded(f"textures/processing/diffuse/{x.replace('dds','png')}")
        if( already ):
            continue

        try:
            with Image.open(f"{config.rtx_remix_dir}/{loadDir}/{x}") as img:
                img.compression = "dxt5"
            
                img.save(f"textures/processing/diffuse/{x.replace('dds','png')}")
                hasherObj.add_loaded(f"textures/processing/diffuse/{x.replace('dds','png')}")
        except Exception as e:
            f = open("logs", "a")
            f.write( "\n"+str(e) )
            f.close()

hasherObj.saveJson()