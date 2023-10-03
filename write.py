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

example_mat = '{"over Shader": {"asset inputs:diffuse_texture": "@./SubUSDs/textures/diffuse/A8D6F2699C10C084.dds@", "custom_inputs:diffuse_texture": {"customData": {"asset default": "@@"}, "displayGroup": "Diffuse", "displayName": "Albedo Map", "doc": "The texture specifying the albedo value and the optional opacity value to use in the alpha channel", "hidden": "false"}, "asset inputs:reflectionroughness_texture": "@./SubUSDs/textures/roughness/A8D6F2699C10C084.dds@", "custom_inputs:reflectionroughness_texture": {"colorSpace": "auto", "customData": {"asset default": "@@"}, "displayGroup": "Specular", "displayName": "Roughness Map", "hidden": "false"}, "asset inputs:normalmap_texture": "@./SubUSDs/textures/normals/A8D6F2699C10C084.dds@", "custom_inputs:normalmap_texture": {"colorSpace": "auto", "customData": {"asset default": "@@"}, "displayGroup": "Normal", "displayName": "Normal Map", "hidden": "false"}, "asset inputs:metallic_texture": "@./SubUSDs/textures/metallness/A8D6F2699C10C084.dds@", "custom_inputs:metallic_texture": {"colorSpace": "auto", "customData": {"asset default": "@@"}, "displayGroup": "Specular", "displayName": "Metallic Map", "hidden": "false"}, "asset inputs:height_texture": "@./SubUSDs/textures/displacements/A8D6F2699C10C084.dds@", "custom_inputs:height_texture": {"colorSpace": "auto", "customData": {"asset default": "@@"}, "displayGroup": "Displacement", "displayName": "Displacement Map", "hidden": "false"}, "float inputs:displace_in": "0.05", "float inputs:transmittance_measurement_distance": "1", "float inputs:reflection_roughness_constant": "1", "float inputs:ior_constant": "0", "float inputs:metallic_constant": "0", "float inputs:emissive_intensity": "0"}}'
mod = ""
RootNode_Looks = {}
mat_names = {}
json_data = {}

def saveAllTextures(mod_dir, replacements_file):
    global mod, RootNode_Looks, mat_names, json_data
    replacements_file = replacements_file.replace("/","")

    replacements_file_dir = f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}"
    isExist = os.path.exists(replacements_file_dir)
    if not isExist:
        nr = open(replacements_file_dir, "w")
        nr.write(replacements)
        nr.close()

    if( mod != mod_dir ):
        usda_data = usda(replacements_file_dir)
        json_data = json.loads( usda_data.returnJson() )
        
        RootNode_Looks = json_data["over RootNode"]["over Looks"]
        mod = mod_dir

    mat_names = list(RootNode_Looks.keys())

    #allMaterials = []
    #pr = open(f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}", "r")
    #prevReplacements = pr.read()
    #pr.close()

    #usda_data = usda(f"{config.rtx_remix_dir}/mods/{mod_dir}/{replacements_file}")
    #print( json.loads( usda_data.returnJson() ) )

    #json_data = usda("{'def Scope Looks': {'def Material AperturePBR_Translucent': {'token outputs:mdl:displacement.connect': '</Looks/AperturePBR_Translucent/Shader.outputs:out>', 'token outputs:mdl:surface.connect': '</Looks/AperturePBR_Translucent/Shader.outputs:out>', 'token outputs:mdl:volume.connect': '</Looks/AperturePBR_Translucent/Shader.outputs:out>', 'def Shader Shader': {'uniform token info:implementationSource': 'sourceAsset', 'uniform asset info:mdl:sourceAsset': '@./SubUSDs/materials/AperturePBR_Translucent.mdl@', 'uniform token info:mdl:sourceAsset:subIdentifier': 'AperturePBR_Translucent', 'float inputs:ior_constant': 1.3, 'custom_inputs:ior_constant': {'customData': {'float default': '1.3', 'dictionary range': {'float max': '3', 'float min': '1'\}\}, 'displayGroup': 'Specular', 'displayName': 'Index of Refraction', 'doc': 'Index of Refraction of the material', 'hidden': 'false'}, 'token outputs:out': {'renderType': 'material'\}\}\}\}, 'over RootNode': {'over Looks': {'over mat_A8D6F2699C10C084': {'over Shader': {'asset inputs:diffuse_texture': '@./SubUSDs/textures/diffuse/A8D6F2699C10C084.dds@', 'custom_inputs:diffuse_texture': {'customData': {'asset default': '@@'}, 'displayGroup': 'Diffuse', 'displayName': 'Albedo Map', 'doc': 'The texture specifying the albedo value and the optional opacity value to use in the alpha channel', 'hidden': 'false'}, 'asset inputs:reflectionroughness_texture': '@./SubUSDs/textures/roughness/A8D6F2699C10C084.dds@', 'custom_inputs:reflectionroughness_texture': {'colorSpace': 'auto', 'customData': {'asset default': '@@'}, 'displayGroup': 'Specular', 'displayName': 'Roughness Map', 'hidden': 'false'}, 'asset inputs:normalmap_texture': '@./SubUSDs/textures/normals/A8D6F2699C10C084.dds@', 'custom_inputs:normalmap_texture': {'colorSpace': 'auto', 'customData': {'asset default': '@@'}, 'displayGroup': 'Normal', 'displayName': 'Normal Map', 'hidden': 'false'}, 'asset inputs:metallic_texture': '@./SubUSDs/textures/metallness/A8D6F2699C10C084.dds@', 'custom_inputs:metallic_texture': {'colorSpace': 'auto', 'customData': {'asset default': '@@'}, 'displayGroup': 'Specular', 'displayName': 'Metallic Map', 'hidden': 'false'}, 'asset inputs:height_texture': '@./SubUSDs/textures/displacements/A8D6F2699C10C084.dds@', 'custom_inputs:height_texture': {'colorSpace': 'auto', 'customData': {'asset default': '@@'}, 'displayGroup': 'Displacement', 'displayName': 'Displacement Map', 'hidden': 'false'}, 'float inputs:displace_in': '0.05', 'float inputs:transmittance_measurement_distance': '1', 'float inputs:reflection_roughness_constant': '1', 'float inputs:ior_constant': '0', 'float inputs:metallic_constant': '0', 'float inputs:emissive_intensity': '0'\}\}\}\}\}")
    
    #print(json_data.json2usda())

    files = 0

    hasherObj = hasher()
    for x in tqdm( os.listdir("textures/processing/diffuse/"), desc="Converting..." ):
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
                try:
                    already = hasherObj.saved(f"textures/processing/upscaled/{x}")
                    if( not already ):
                        with image.Image(filename=f"textures/processing/diffuse/{x}") as img:
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



            
            mat_to_edit = []
            mat_selected_name = x.replace('.png','')

            f = open(f"materials/{x.replace('.png','.mat')}","r")
            material_properties = f.read().split("\n")
            f.close()
            

            if( f"over mat_{mat_selected_name}" not in mat_names ):
                mat_to_edit = json.loads( example_mat )
                mat_names.append(f"over mat_{mat_selected_name}")
            else:
                mat_to_edit = RootNode_Looks[ f"over mat_{mat_selected_name}" ]

        
            mat_to_edit["over Shader"]["asset inputs:diffuse_texture"] = f"@./SubUSDs/textures/diffuse/{mat_selected_name}.dds@"
            mat_to_edit["over Shader"]["asset inputs:reflectionroughness_texture"] = f"@./SubUSDs/textures/roughness/{mat_selected_name}.dds@"
            mat_to_edit["over Shader"]["asset inputs:normalmap_texture"] = f"@./SubUSDs/textures/normals/{mat_selected_name}.dds@"
            mat_to_edit["over Shader"]["asset inputs:metallic_texture"] = f"@./SubUSDs/textures/metallness/{mat_selected_name}.dds@"
            mat_to_edit["over Shader"]["asset inputs:height_texture"] = f"@./SubUSDs/textures/displacements/{mat_selected_name}.dds@"

            temp_ref = {}
            if( material_properties[0] == "@glass" ):
                if( f"custom_over mat_{mat_selected_name}" not in mat_names ):
                    temp_ref["references"] = "@./SubUSDs/AperturePBR_Translucent.usda@</Looks/mat_AperturePBR_Translucent>"
                    if( RootNode_Looks.get(f"parameters_over mat_{mat_selected_name}") != None ):
                        RootNode_Looks.pop(f"parameters_over mat_{mat_selected_name}")
                
                mat_to_edit["over Shader"]["uniform asset info:mdl:sourceAsset"] = "@AperturePBR_Translucent.mdl@"
            elif( material_properties[0] == "@emissive" ):
                if( f"custom_over mat_{mat_selected_name}" in mat_names ):
                    RootNode_Looks.pop(f"custom_over mat_{mat_selected_name}")
                if( "uniform asset info:mdl:sourceAsset" in mat_to_edit["over Shader"] ):
                    RootNode_Looks["over Shader"].pop("uniform asset info:mdl:sourceAsset")

                RootNode_Looks[f"parameters_over mat_{mat_selected_name}"] = temp_ref
                mat_to_edit["over Shader"]["asset inputs:emissive_mask_texture"] = f"@./SubUSDs/textures/diffuse/{mat_selected_name}.dds@"
                mat_to_edit["over Shader"]["bool inputs:enable_emission"] = 1
            else:
                if( f"custom_over mat_{mat_selected_name}" in mat_names ):
                    RootNode_Looks.pop(f"custom_over mat_{mat_selected_name}")
                if( "uniform asset info:mdl:sourceAsset" in mat_to_edit["over Shader"] ):
                    RootNode_Looks["over Shader"].pop("uniform asset info:mdl:sourceAsset")

                mat_to_edit["over Shader"]["bool inputs:enable_emission"] = 0

            for y in range( 1, len(material_properties) ):
                temp_var_data = material_properties[y].replace(" ","").split("=")
                var_name = temp_var_data[0]
                var_value = temp_var_data[1]
                mat_to_edit["over Shader"][f"float inputs:{var_name}"] = var_value

            RootNode_Looks[ f"over mat_{mat_selected_name}" ] = mat_to_edit


    RootNode_Looks = RootNode_Looks
    json_data["over RootNode"]["over Looks"] = RootNode_Looks

    hasherObj.saveJson()

    json_data_dumps = json.dumps( json_data )
    usda_back = usda(json_data_dumps)
    usda_back = usda_back.json2usda()

    print("\nWriting replacements...")
    nr = open(replacements_file_dir, "w")
    nr.write(usda_back)
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

