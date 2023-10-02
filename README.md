<img src="https://i.imgur.com/U40OgUz.png" alt="logo" width="250px" height="250px">

# OctoTex
This tool is heavily experimental!

## Description
This tool allows you to load captured textures from rtx remix, convert them to png, upscale with ESRGAN or RealESRGAN, generate octahedral normals, roughness, metalness maps, and write it back to the existing rtx remix mod, or create a new one ( recomended )

## AI PBR Models
You can download ai models from my <a href="https://drive.google.com/file/d/1AKyWlZ75V0T6SvhaLwwIiCrJL3Cl_-s2/view?usp=sharing" >google drive</a>

Put the models to the
  1. OctoTex/ai/PBR/checkpoints/disp
  2. OctoTex/ai/PBR/checkpoints/norm
  3. OctoTex/ai/PBR/checkpoints/rough
Folders!

## Attention
If you don't want or cannot use upscaler, just drag all the textures from remixer/textures/processing/diffuse folder to the remixer/textures/processing/upscaled folder.
For the first time, all of the steps may take a while, then the process will be faster.

## New Steps
1. python webui.py      // That's it!

## Outdated Steps
1. python load.py ( then select from what folder you want to load textures )                   // Textures will be in the textures/processing/diffuse folder
2. python upscale.py ( you will need an Nvidia GPU, pytorch with cuda support installed )      // Textures will be in the textures/processing/upscaled folder
3. python pbr.py ( this will generate all the pbr textures to the their folders )              // Textures will be in the textures/processing/normals ** roughness ** metallness folders
4. python write.py ( this will write all the changes back, it will promt to what mod you want to write it, IT'S RECOMENDED TO CREATE A NEW MOD! )
And that's it!

Good luck! :)


This project is possible because my boss gave me an RTX gpu, and allowed me to work on this project in office some time, so, i'll be glad if you check his website, thanks!
https://fst.kz/
