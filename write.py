import os
from tqdm import tqdm
import config
from hash.hasher import *
from mods.controller import *
from wand import image


replacements = """#usda 1.0
(
    upAxis = "Y"
)

def Scope "Looks"
{
    def Material "AperturePBR_Translucent"
    {
        token outputs:mdl:displacement.connect = </Looks/AperturePBR_Translucent/Shader.outputs:out>
        token outputs:mdl:surface.connect = </Looks/AperturePBR_Translucent/Shader.outputs:out>
        token outputs:mdl:volume.connect = </Looks/AperturePBR_Translucent/Shader.outputs:out>

        def Shader "Shader"
        {
            uniform token info:implementationSource = "sourceAsset"
            uniform asset info:mdl:sourceAsset = @./SubUSDs/materials/AperturePBR_Translucent.mdl@
            uniform token info:mdl:sourceAsset:subIdentifier = "AperturePBR_Translucent"
            float inputs:ior_constant = 1.3 (
                customData = {
                    float default = 1.3
                    dictionary range = {
                        float max = 3
                        float min = 1
                    }
                }
                displayGroup = "Specular"
                displayName = "Index of Refraction"
                doc = "Index of Refraction of the material"
                hidden = false
            )
            token outputs:out (
                renderType = "material"
            )
        }
    }
}

over "RootNode"
{
    over "Looks"
    {
        $first_mat$
    }
}
"""

example_mat = """$filename$"
        {
            over "Shader"
            {
                asset inputs:diffuse_texture = @./SubUSDs/textures/diffuse/$filename$.dds@ (
                    customData = {
                        asset default = @@
                    }
                    displayGroup = "Diffuse"
                    displayName = "Albedo Map"
                    doc = "The texture specifying the albedo value and the optional opacity value to use in the alpha channel"
                    hidden = false
                )
                asset inputs:reflectionroughness_texture = @./SubUSDs/textures/roughness/$filename$.dds@ (
                    colorSpace = "auto"
                    customData = {
                        asset default = @@
                    }
                    displayGroup = "Specular"
                    displayName = "Roughness Map"
                    hidden = false
                )
                asset inputs:normalmap_texture = @./SubUSDs/textures/normals/$filename$.dds@ (
                    colorSpace = "auto"
                    customData = {
                        asset default = @@
                    }
                    displayGroup = "Normal"
                    displayName = "Normal Map"
                    hidden = false
                )
                asset inputs:metallic_texture = @./SubUSDs/textures/metallness/$filename$.dds@ (
                    colorSpace = "auto"
                    customData = {
                        asset default = @@
                    }
                    displayGroup = "Specular"
                    displayName = "Metallic Map"
                    hidden = false
                )
                asset inputs:height_texture = @./SubUSDs/textures/displacements/$filename$.dds@ (
                    colorSpace = "auto"
                    customData = {
                        asset default = @@
                    }
                    displayGroup = "Displacement"
                    displayName = "Displacement Map"
                    hidden = false
                )
                float inputs:transmittance_measurement_distance = 65504
                float inputs:reflection_roughness_constant = 1
                float inputs:displace_in = 0.05
            }
        }
"""

def saveAllTextures(mod_dir, replacements_file):
    replacements_file = replacements_file.replace("/","")

    #allMaterials = []
    pr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}", "r")
    prevReplacements = pr.read()
    pr.close()
    files = 0

    hasherObj = hasher()
    for x in tqdm( os.listdir("textures/processing/upscaled/"), desc="Converting..." ):
        if x.endswith(".png"):
            try:
                already = hasherObj.saved(f"textures/processing/upscaled/{x}")
                if( not already ):
                    with image.Image(filename=f"textures/processing/upscaled/{x}") as img:
                        img.compression = "dxt5"
                        img.save(filename=f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/textures/diffuse/{x.replace('png','dds')}")
                        hasherObj.add_saved(f"textures/processing/upscaled/{x}")
                        files += 1
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()

            try:
                already = hasherObj.saved(f"textures/processing/metallness/{x.replace('.png','')}_metal.png")
                if( not already ):
                    with image.Image(filename=f"textures/processing/metallness/{x.replace('.png','')}_metal.png") as img:
                        img.compression = "dxt5"
                        img.save(filename=f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/textures/metallness/{x.replace('png','dds')}")
                        hasherObj.add_saved(f"textures/processing/metallness/{x.replace('.png','')}_metal.png")
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()


            try:
                already = hasherObj.saved(f"textures/processing/normals/{x.replace('.png','')}_normal.png")
                if( not already ):
                    with image.Image(filename=f"textures/processing/normals/{x.replace('.png','')}_normal.png") as img:
                        img.compression = "dxt5"
                        img.save(filename=f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/textures/normals/{x.replace('png','dds')}")
                        hasherObj.add_saved(f"textures/processing/normals/{x.replace('.png','')}_normal.png")
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()

            try:
                already = hasherObj.saved(f"textures/processing/roughness/{x.replace('.png','')}_rough.png")
                if( not already ):
                    with image.Image(filename=f"textures/processing/roughness/{x.replace('.png','')}_rough.png") as img:
                        img.compression = "dxt5"
                        img.save(filename=f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/textures/roughness/{x.replace('png','dds')}")
                        hasherObj.add_saved(f"textures/processing/roughness/{x.replace('.png','')}_rough.png")
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()

            try:
                already = hasherObj.saved(f"textures/processing/displacements/{x.replace('.png','')}_disp.png")
                if( not already ):
                    with image.Image(filename=f"textures/processing/displacements/{x.replace('.png','')}_disp.png") as img:
                        img.compression = "dxt5"
                        img.save(filename=f"{config.rtx_remix_dir}/mods/{mod_dir}/SubUSDs/textures/displacements/{x.replace('png','dds')}")
                        hasherObj.add_saved(f"textures/processing/displacements/{x.replace('.png','')}_disp.png")
            except Exception as e:
                f = open("logs", "a")
                f.write( "\n"+str(e) )
                f.close()

            add_mat = example_mat.replace("$filename$",x.replace('.png',''))

            if( "over \"RootNode\"" not in prevReplacements ):
                prevReplacements = replacements.replace("$first_mat$","over \"mat_" + add_mat)
            else:
                if( "mat_" not in prevReplacements ):
                    prevReplacements = prevReplacements.replace("""    over "Looks"
    {""","""    over "Looks"
    {
        over \"mat_""" + add_mat)

                else:
                    if( "mat_" + x.replace('.png','') not in prevReplacements ):
                        splitted = prevReplacements.split("over \"mat_")
                        splitted.insert(1,add_mat)

                        prevReplacements = "over \"mat_".join(splitted)

            #allMaterials.append(  )
            f = open(f"materials/{x.replace('.png','.mat')}","r")
            material_properties = f.read().split("\n")
            f.close()
            

            if( material_properties[0] == "@glass" ):
                if( "SubUSDs/AperturePBR_Translucent.usda@</Looks/mat_AperturePBR_Translucent" not in prevReplacements ):
                    prevReplacements = prevReplacements.replace(f"over \"mat_{x.replace('.png','')}\"",f"""over \"mat_{x.replace('.png','')}\"( 
        references = @./SubUSDs/AperturePBR_Translucent.usda@</Looks/mat_AperturePBR_Translucent>
    )""" )
            elif( material_properties[0] == "@opaque" ):
                prevReplacements = prevReplacements.replace(f"""over \"mat_{x.replace('.png','')}\"( 
        references = @./SubUSDs/AperturePBR_Translucent.usda@</Looks/mat_AperturePBR_Translucent>
    )""", f"over \"mat_{x.replace('.png','')}\"" )
            
            body = prevReplacements.split(f"over \"mat_{x.replace('.png','')}\"")[1]
            body = body.split("""            }
        }""")[0]
            backup = body
            #print(body)
            variables = body.split("\n")
            material_properties.append("@AperturePBR_Translucent.mdl@")
            
            for z in range( 1, len(material_properties) ):
                for y in range( len(variables)-1 ):
                    if( material_properties[z].split(" ")[0] in variables[y]):
                        variables.pop(y)

            variables.pop(-1)

            for y in range( 1, len(material_properties)-1 ):
                variables.append(f"                float inputs:{material_properties[y]}")


            if( material_properties[0] == "@glass" ):
                variables.append("                uniform asset info:mdl:sourceAsset = @AperturePBR_Translucent.mdl@" )
  
            body = "\n".join(variables)
            if( material_properties[0] == "@opaque" ):
                body = body.replace("uniform asset info:mdl:sourceAsset = @AperturePBR_Translucent.mdl@", "" )
            

            prevReplacements = prevReplacements.replace(backup,body + "\n")

    hasherObj.saveJson()


    print("\nWriting replacements...")
    nr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}", "w")
    nr.write(prevReplacements)
    nr.close()
    print("Done!")

    nr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/mod.usda", "r")
    data = nr.read()
    nr.close()

    nr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/mod.usda", "w")
    nr.write(data)
    nr.close()

    return files


if __name__ == '__main__':
    mod_dir, replacements_file = modFolder()
    saveAllTextures(mod_dir, replacements_file)

