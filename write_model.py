import os
from tqdm import tqdm
import config
from hash.hasher import *
from mods.controller import *
from wand import image
from usda import usda


replacements = """#usda 1.0
(
    upAxis = "Y"
)

over "RootNode"
{
    over "meshes"
    {
        $newdata$
    }
}
"""

    
example_mesh = """        
        over Xform "$name$"(
            prepend references = @./SubUSDs/meshes/$name$.usda@
        )
        {
        }
"""

example_usda = """#usda 1.0
(
    customLayerData = {
        uint64 geometrydescriptor = 15755592595057390902
        uint64 indices = 0
        uint64 legacyindices = 0
        uint64 legacypositions0 = 0
        uint64 legacypositions1 = 0
        uint64 positions = 5445149271889707011
        uint64 texcoords = 16764550512849261066
        uint64 vertexlayout = 5377511480456297298
        uint64 vertexshader = 0
    }
    defaultPrim = "$mesh$"
    doc = "Generated"
    metersPerUnit = 1
    timeCodesPerSecond = 24
    upAxis = "Y"
)

over Xform "$mesh$"
{
    token visibility = "inherited"

    over Mesh "mesh"
    {
        uniform bool doubleSided = 0
        int[] faceVertexCounts = [$faceVertexCounts$]
        int[] faceVertexIndices = [$faceVertexIndices$]
        normal3f[] normals = [$normals$]
        uniform token orientation = "leftHanded"
        point3f[] points = [$points$]
        texCoord2f[] primvars:st = [$uvs$] (
            interpolation = "vertex"
        )
        uniform token subdivisionScheme = "none"
        token visibility = "inherited"
    }
}

"""

mod = ""
RootNode_Looks = {}
mat_names = {}
json_data = {}

def saveAllTextures(mod_dir, replacements_file):
    global mod, RootNode_Looks, mat_names, json_data
    replacements_file = "/meshes.usda"
    replacements_file = replacements_file.replace("/","")

    replacements_file_dir = f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}"
    isExist = os.path.exists(replacements_file_dir)
    usda_back = ""


    hasherObj = hasher()
    for x in tqdm( os.listdir("meshes/"), desc="Converting..." ):
        if x.endswith(".obj"):
            f = open(f"meshes/{x}", "r")
            data = f.read()
            f.close()

            points = ""
            normals = ""
            uvs = ""
            faceVertexIndices = ""
            faceVertexCounts = ""

            splitted = data.split("\n")
            for y in range(len(splitted)):
                temp = splitted[y]
                if( len( temp ) < 1 ):
                    continue

                if( temp[0] == "v" and temp[1] != "t" and temp[1] != "n" ):
                    points += "(" + temp.replace("v ","").replace(" ",",") + "),"
                    continue

                if( temp[0] == "v" and temp[1] == "n" ):
                    normals += "(" + temp.replace("vn ","").replace(" ",",") + "),"
                    continue

                if( temp[0] == "v" and temp[1] == "t" ):
                    uvs += "(" + temp.replace("vt ","").replace(" ",",") + "),"
                    continue

                if( temp[0] == "f" ):
                    faceVertexCounts += "3,"
                    tempFace = temp.replace("f ","").replace(" ","/").split("/")
                    faceVertexIndices += tempFace[0] + "," + tempFace[2] + "," + tempFace[4] + ","
                    continue    

            normals = normals[:-1]
            points = points[:-1]
            uvs = uvs[:-1]
            faceVertexCounts = faceVertexCounts[:-1]
            faceVertexIndices = faceVertexIndices[:-1]

            f = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/meshes/" + x.replace(".obj",".usda"), "w")
            f.write( example_usda.replace("$mesh$",x.replace(".obj","")).replace("$points$",points).replace("$uvs$",uvs).replace("$normals$",normals).replace("$faceVertexCounts$",faceVertexCounts).replace("$faceVertexIndices$",faceVertexIndices) ) 
            f.close()

            




            newData = example_mesh.replace("$name$",x.replace(".obj",""))
            usda_back = usda_back + newData



    print("\nWriting replacements...")
    nr = open(replacements_file_dir, "w")
    nr.write( replacements.replace("$newdata$",usda_back) )
    nr.close()
    print("Done!")

    nr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/mod.usda", "r")
    data = nr.read()
    nr.close()

    nr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/mod.usda", "w")
    nr.write(data)
    nr.close()

    #return files


if __name__ == '__main__':
    mod_dir, replacements_file = modFolder()
    saveAllTextures(mod_dir, replacements_file)

