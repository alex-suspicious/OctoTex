from PIL import Image
import os
from tqdm import tqdm
import config
from hash.hasher import *
import pathlib

loadDirId = 0
loadDir = "captures"

neededDirectories = ["textures","meshes","meshes/usda","textures/processing","textures/processing/upscaled","textures/processing/roughness","textures/processing/displacements","textures/processing/normaldx","textures/processing/normals","textures/processing/metallness","textures/processing/emission","textures/processing/diffuse",f"{config.rtx_remix_dir}/mods"]

for directory in neededDirectories:
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)

def loadTextures(loadDir, updateFunction = 0, show = 0, close = 0 ):
    hasherObj = hasher()
    dirList = os.listdir(f"{config.rtx_remix_dir}/{loadDir}/")
    steps = 0
    success = 0

    if( show ):
        show()

    for x in tqdm( dirList, desc="Converting..." ):
        if x.endswith(".dds"):
            already = hasherObj.loaded(f"textures/processing/diffuse/{x.replace('dds','png')}")
            if( already ):
                continue

            if( updateFunction ):
                updateFunction( len(dirList), steps )

            try:
                with Image.open(f"{config.rtx_remix_dir}/{loadDir}/{x}") as img:
                    img.compression = "dxt5"
                
                    img.save(f"textures/processing/diffuse/{x.replace('dds','png')}")
                    hasherObj.add_loaded(f"textures/processing/diffuse/{x.replace('dds','png')}")
                    success += 1
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()
            
            steps += 1

    if( close ):
        close(success)

    hasherObj.saveJson()
    return success

def loadSingleTexture(loadFile):
    hasherObj = hasher()
    loadFilePath = f"{config.rtx_remix_dir}/{loadDir}/{loadFile}.dds"


    already = hasherObj.loaded(f"textures/processing/diffuse/{loadFile.replace('dds','png')}")
    if( already ):
        return 0

    try:
        with Image.open(loadFilePath) as img:
            img.compression = "dxt5"
        
            img.save(f"textures/processing/diffuse/{x.replace('dds','png')}")
            hasherObj.add_loaded(f"textures/processing/diffuse/{x.replace('dds','png')}")
    except Exception as e:
        return 0

    hasherObj.saveJson()
    return 1

if __name__ == '__main__':
    mods = [f for f in pathlib.Path().glob(f"{config.rtx_remix_dir}/mods/*")]
    if( len(mods) > 0 ):
        print("Directories for importing: ")

        print("0 | captures")
        for x in range(len(mods)):
            mod_path = str(mods[x]).replace(f"{config.rtx_remix_dir}/mods/","")
            print(f"{x+1} | {mod_path}")


        loadDirId = int(input("From what dir you want to load the textures, select by index: "))
        loadDirId -= 1
        if( loadDirId != -1 ):
            loadDir = str(mods[loadDirId]).replace(f"{config.rtx_remix_dir}/","") + "/SubUSDs/textures/diffuse"
        else:
            loadDir += "/textures"
    else:
        loadDir += "/textures"

    loadTextures(loadDir)