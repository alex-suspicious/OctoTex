import pathlib
import config
import json

def modFolder():
	mods = [f for f in pathlib.Path().glob("../rtx-remix/mods/*")]
	if( len(mods) > 0 ):
		print("Here's your mods:")
	else:
		return

	for x in range(len(mods)):
		mod_path = str(mods[x]).replace("../rtx-remix/mods/","")
		print(f"{x} | {mod_path}")

	dirId = 0
	dirId = int(input("Select the mod that you want to write by index: "))

	mod_dir = mods[dirId]
	print(f"Selected mod: {str(mod_dir).replace('../rtx-remix/mods/','')}")

	jsonFile = open("mods/saved.json","r")
	jsonData = jsonFile.read()
	jsonFile.close()
	savedMods = json.loads(jsonData)

	returnModDir = str(mod_dir).replace('../rtx-remix/mods/','')
	config.selected_mod = str(mod_dir).replace('../rtx-remix/mods/','')

	if( returnModDir in savedMods ):
		return returnModDir, savedMods[returnModDir]

	print("\nNow select the replacements file that you want to write\nThis message will appear only once, the settings will be saved")
	replacements = [f for f in pathlib.Path().glob(f"{mod_dir}/*.usda")]

	for x in range(len(replacements)):
		replacement_path = str(replacements[x]).replace(str(mod_dir),"")
		print(f"{x} | {replacement_path}")

	repId = 0
	repId = int(input("Select the replacements file that you want to write by index: "))
	replacement_file = replacements[repId]
	
	returnConfigName = str(replacement_file).replace(f'../rtx-remix/mods/{returnModDir}','')
	savedMods[returnModDir] = returnConfigName
	
	jsonData = json.dumps( savedMods )

	jsonFile = open("mods/saved.json","w")
	jsonFile.write(jsonData)
	jsonFile.close()

	return returnModDir, returnConfigName