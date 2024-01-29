
<img src="https://i.imgur.com/xoEqTaZ.png" alt="logo" width="250px" height="250px">

# Re-Tex - supporting OctoTex
This tool will be heavily upgraded!

## Description
This tool allows you to load captured textures from rtx remix, convert them to png, upscale with ESRGAN or RealESRGAN, generate octahedral normals, roughness, metalness maps, and write it back to the existing rtx remix mod, or create a new one ( recomended ). 

## AI PBR Models
You can download old PBR ai models from Alex's <a href="https://drive.google.com/file/d/1AKyWlZ75V0T6SvhaLwwIiCrJL3Cl_-s2/view?usp=sharing" >Gdrive</a> and from <a href="https://drive.google.com/file/d/1FAUugbC8uMSiSzm0FtR-Wa3pP81zXz3H/view?usp=sharing" > mine Gdrive</a>

Put the old models to the
  1. OctoTex/ai/PBR/checkpoints/disp
  2. OctoTex/ai/PBR/checkpoints/norm
Folders!

And <a href="https://drive.google.com/file/d/1TCZMfdwbGkxw1nfpAIc2c8_iGSPRu0FO/view?usp=sharing" >New Roughness Model on Gdrive</a>

Put the new model to the
  1. OctoTex/ai/PBR/checkpoints/rough
Folder!


## New Steps
1. python webui.py      // That's it!

## Outdated Steps
1. python load.py ( then select from what folder you want to load textures )                   // Textures will be in the textures/processing/diffuse folder
2. python upscale.py ( you will need an Nvidia GPU, pytorch with cuda support installed )      // Textures will be in the textures/processing/diffuse folder
3. python pbr.py ( this will generate all the pbr textures to the their folders )              // Textures will be in the textures/processing/normals ** roughness ** metallness folders
4. python write.py ( this will write all the changes back, it will promt to what mod you want to write it, IT'S RECOMENDED TO CREATE A NEW MOD! )
And that's it!

## TO DO
1. Train models
2. Make upscaler

   
Good luck! :)

By Alex:

> This project is possible because my boss gave me an RTX gpu, and
> allowed me to work on this project in office some time, so, i'll be
> glad if you check his website, thanks! https://fst.kz/

