# BE CAREFUL!
# This script will update all hashes!

for x in tqdm( os.listdir(f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/upscaled/"), desc="Generating..." ):
	if x.endswith(".png"):
		generate_normal(
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/upscaled/{x}",
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/normals/{x.replace('.png','_normal')}.png",0,1.5)

		generate_roughness(
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/upscaled/{x}",
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/roughness/{x.replace('.png','_rough')}.png",1)

		generate_metalness(
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/upscaled/{x}",
			f"{config.rtx_remix_dir}/mods/gameReadyAssets/SubUSDs/processing/metallness/{x.replace('.png','_metal')}.png",1)
