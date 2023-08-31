Hello reader!
Ok heres what you need to know, first things first, you need to capture textures in game using remix, if you did this already, read the next lines.
Open the remixer folder in cmd ( terminal ) and write the next commands:

python3 load.py
// This will load all the textures to the remixer/textures/processing/diffuse folder as .png files

python3 upscale.py
// This will upscale all the textures in remixer/textures/processing/diffuse folder and saves them in remixer/textures/processing/upscaled folder

python3 pbr.py
// This will generate normal, roughness and metal map for textures in remixer/textures/processing/upscaled folder, all the maps will be located in the their types folders, if it's normal map, then it'll be remixer/textures/processing/normals and etc


// After you've done everything without errors, use this
python3 write.py
// This will convert all your textures, normals, and roughness to DDS files, put them to the mod folder, and adds material to the replacements.usda file AUTOMATICALLY!


P.S If you don't want or cannot use upscaler, just drag all the textures from remixer/textures/processing/diffuse folder to the remixer/textures/processing/upscaled folder.
For the first time, all of the steps may take a while, if you have a high quality textures or alot of them, you need to wait, then the process will be faster.
Good luck! :)

This project is possible because my boss gave me an RTX gpu, and allowed me to work on this project in office some time, so, i'll be glad if you check his website, thanks!
https://fst.kz/
