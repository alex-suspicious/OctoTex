
<img src="https://i.imgur.com/U40OgUz.png" alt="logo" width="250px" height="250px">

# OctoTex
This tool is heavily experimental!

## Description
This tool allows you to load captured textures from rtx remix, convert them to png, upscale with ESRGAN or RealESRGAN, generate octahedral normals, roughness, metalness maps, and write it back to the existing rtx remix mod, or create a new one ( recomended ). 

## AI PBR Models
You can download ai models from Alex's <a href="https://drive.google.com/file/d/1AKyWlZ75V0T6SvhaLwwIiCrJL3Cl_-s2/view?usp=sharing" >Gdrive</a> and from <a href="https://drive.google.com/file/d/1FAUugbC8uMSiSzm0FtR-Wa3pP81zXz3H/view?usp=sharing" > mine Gdrive</a> and <a href="magnet:?xt=urn:btih:ad8299193c57e8f444b2295615359c6e770726d9&dn=checkpoints.zip&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969%2Fannounce&tr=http%3A%2F%2F104.28.1.30%3A8080%2Fannounce&tr=http%3A%2F%2F104.28.16.69%2Fannounce&tr=udp%3A%2F%2F107.150.14.110%3A6969%2Fannounce&tr=udp%3A%2F%2F109.121.134.121%3A1337%2Fannounce&tr=udp%3A%2F%2F114.55.113.60%3A6969%2Fannounce&tr=http%3A%2F%2F125.227.35.196%3A6969%2Fannounce&tr=udp%3A%2F%2F128.199.70.66%3A5944%2Fannounce&tr=http%3A%2F%2F157.7.202.64%3A8080%2Fannounce&tr=http%3A%2F%2F158.69.146.212%3A7777%2Fannounce&tr=http%3A%2F%2F173.254.204.71%3A1096%2Fannounce&tr=http%3A%2F%2F178.175.143.27%2Fannounce&tr=udp%3A%2F%2F178.33.73.26%3A2710%2Fannounce&tr=udp%3A%2F%2F182.176.139.129%3A6969%2Fannounce&tr=udp%3A%2F%2F185.5.97.139%3A8089%2Fannounce&tr=udp%3A%2F%2F188.165.253.109%3A1337%2Fannounce&tr=udp%3A%2F%2F194.106.216.222%3A80%2Fannounce&tr=udp%3A%2F%2F195.123.209.37%3A1337%2Fannounce&tr=http%3A%2F%2F210.244.71.25%3A6969%2Fannounce&tr=http%3A%2F%2F210.244.71.26%3A6969%2Fannounce&tr=http%3A%2F%2F213.159.215.198%3A6970%2Fannounce&tr=udp%3A%2F%2F213.163.67.56%3A1337%2Fannounce&tr=http%3A%2F%2F37.19.5.139%3A6969%2Fannounce&tr=udp%3A%2F%2F37.19.5.155%3A2710%2Fannounce&tr=udp%3A%2F%2F46.4.109.148%3A6969%2Fannounce&tr=udp%3A%2F%2F5.79.249.77%3A6969%2Fannounce&tr=udp%3A%2F%2F5.79.83.193%3A6969%2Fannounce&tr=udp%3A%2F%2F51.254.244.161%3A6969%2Fannounce&tr=http%3A%2F%2F59.36.96.77%3A6969%2Fannounce&tr=udp%3A%2F%2F74.82.52.209%3A6969%2Fannounce&tr=http%3A%2F%2F80.246.243.18%3A6969%2Fannounce&tr=http%3A%2F%2F81.200.2.231%2Fannounce&tr=udp%3A%2F%2F85.17.19.180%3A80%2Fannounce&tr=http%3A%2F%2F87.248.186.252%3A8080%2Fannounce&tr=http%3A%2F%2F87.253.152.137%2Fannounce&tr=http%3A%2F%2F91.216.110.47%2Fannounce&tr=http%3A%2F%2F91.217.91.21%3A3218%2Fannounce&tr=udp%3A%2F%2F91.218.230.81%3A6969%2Fannounce&tr=http%3A%2F%2F93.92.64.5%2Fannounce&tr=http%3A%2F%2Fatrack.pow7.com%2Fannounce&tr=http%3A%2F%2Fbt.henbt.com%3A2710%2Fannounce&tr=http%3A%2F%2Fbt.pusacg.org%3A8080%2Fannounce&tr=http%3A%2F%2Fbt2.careland.com.cn%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fmgtracker.org%3A2710%2Fannounce&tr=http%3A%2F%2Fmgtracker.org%3A6969%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=http%3A%2F%2Fopen.lolicon.eu%3A7777%2Fannounce&tr=http%3A%2F%2Fopen.touki.ru%2Fannounce.php&tr=http%3A%2F%2Fp4p.arenabg.ch%3A1337%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=http%3A%2F%2Fpow7.com%3A80%2Fannounce&tr=http%3A%2F%2Fretracker.gorcomnet.ru%2Fannounce&tr=http%3A%2F%2Fretracker.krs-ix.ru%2Fannounce&tr=http%3A%2F%2Fretracker.krs-ix.ru%3A80%2Fannounce&tr=http%3A%2F%2Fsecure.pow7.com%2Fannounce&tr=http%3A%2F%2Ft1.pow7.com%2Fannounce&tr=http%3A%2F%2Ft2.pow7.com%2Fannounce&tr=http%3A%2F%2Fthetracker.org%3A80%2Fannounce&tr=udp%3A%2F%2Ftorrent.gresille.org%3A80%2Fannounce&tr=http%3A%2F%2Ftorrentsmd.com%3A8080%2Fannounce&tr=udp%3A%2F%2Ftracker.aletorrenty.pl%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.baravik.org%3A6970%2Fannounce&tr=udp%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.bittorrent.am%2Fannounce&tr=http%3A%2F%2Ftracker.calculate.ru%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.dutchtracking.com%2Fannounce&tr=http%3A%2F%2Ftracker.dutchtracking.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.dutchtracking.nl%2Fannounce&tr=http%3A%2F%2Ftracker.dutchtracking.nl%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.edoardocolombo.eu%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.ex.ua%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.ex.ua%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.filetracker.pl%3A8089%2Fannounce&tr=udp%3A%2F%2Ftracker.flashtorrents.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.grepler.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.kicks-ass.net%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.kicks-ass.net%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.kuroy.me%3A5944%2Fannounce&tr=udp%3A%2F%2Ftracker.mg64.net%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.skyts.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.tfile.me%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.tvunderground.org.ru%3A3218%2Fannounce&tr=udp%3A%2F%2Ftracker.yoshi210.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker1.wasabii.com.tw%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker2.wasabii.com.tw%3A6969%2Fannounce&tr=http%3A%2F%2Fwww.wareztorrent.com%2Fannounce&tr=http%3A%2F%2Fwww.wareztorrent.com%3A80%2Fannounce&tr=https%3A%2F%2F104.28.17.69%2Fannounce&tr=https%3A%2F%2Fwww.wareztorrent.com%2Fannounce&tr=http%3A%2F%2F107.150.14.110%3A6969%2Fannounce&tr=http%3A%2F%2F109.121.134.121%3A1337%2Fannounce&tr=http%3A%2F%2F114.55.113.60%3A6969%2Fannounce&tr=http%3A%2F%2F128.199.70.66%3A5944%2Fannounce&tr=udp%3A%2F%2F151.80.120.114%3A2710%2Fannounce&tr=udp%3A%2F%2F168.235.67.63%3A6969%2Fannounce&tr=http%3A%2F%2F178.33.73.26%3A2710%2Fannounce&tr=http%3A%2F%2F182.176.139.129%3A6969%2Fannounce&tr=http%3A%2F%2F185.5.97.139%3A8089%2Fannounce&tr=udp%3A%2F%2F185.86.149.205%3A1337%2Fannounce&tr=http%3A%2F%2F188.165.253.109%3A1337%2Fannounce&tr=udp%3A%2F%2F191.101.229.236%3A1337%2Fannounce&tr=http%3A%2F%2F194.106.216.222%2Fannounce&tr=http%3A%2F%2F195.123.209.37%3A1337%2Fannounce&tr=udp%3A%2F%2F195.123.209.40%3A80%2Fannounce&tr=udp%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=http%3A%2F%2F213.163.67.56%3A1337%2Fannounce&tr=http%3A%2F%2F37.19.5.155%3A6881%2Fannounce&tr=http%3A%2F%2F46.4.109.148%3A6969%2Fannounce&tr=http%3A%2F%2F5.79.249.77%3A6969%2Fannounce&tr=http%3A%2F%2F5.79.83.193%3A2710%2Fannounce&tr=http%3A%2F%2F51.254.244.161%3A6969%2Fannounce&tr=udp%3A%2F%2F62.138.0.158%3A6969%2Fannounce&tr=udp%3A%2F%2F62.212.85.66%3A2710%2Fannounce&tr=http%3A%2F%2F74.82.52.209%3A6969%2Fannounce&tr=http%3A%2F%2F85.17.19.180%2Fannounce&tr=udp%3A%2F%2F89.234.156.205%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=http%3A%2F%2F91.218.230.81%3A6969%2Fannounce&tr=udp%3A%2F%2F94.23.183.33%3A6969%2Fannounce&tr=udp%3A%2F%2Fbt.xxx-tracker.com%3A2710%2Fannounce&tr=udp%3A%2F%2Feddie4.nl%3A6969%2Fannounce&tr=http%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=http%3A%2F%2Fmgtracker.org%3A2710%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fshadowshq.eddie4.nl%3A6969%2Fannounce&tr=udp%3A%2F%2Fshadowshq.yi.org%3A6969%2Fannounce&tr=http%3A%2F%2Ftorrent.gresille.org%2Fannounce&tr=http%3A%2F%2Ftracker.aletorrenty.pl%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.eddie4.nl%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.ex.ua%2Fannounce&tr=http%3A%2F%2Ftracker.filetracker.pl%3A8089%2Fannounce&tr=http%3A%2F%2Ftracker.flashtorrents.org%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.grepler.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.ilibr.org%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.kicks-ass.net%2Fannounce&tr=http%3A%2F%2Ftracker.kuroy.me%3A5944%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.mg64.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.mg64.net%3A6881%2Fannounce&tr=http%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.piratepublic.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.sktorrent.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.skyts.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.yoshi210.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker2.indowebster.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker4.piratux.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fzer0day.ch%3A1337%2Fannounce&tr=udp%3A%2F%2Fzer0day.to%3A1337%2Fannounce&ws=https://doc-0c-bo-docs.googleusercontent.com/docs/securesc/qhekgciv309h4oprpehp55qr5ss9cr1c/7uqeud544lavk92s9sqqn537fvft0k44/1699250475000/02775174769506565063/02775174769506565063/1FAUugbC8uMSiSzm0FtR-Wa3pP81zXz3H?e=download&ax=AI0foUqLdC9uv7C1CvrXZs_OK56BVIoqA8xF-qzPNXA59Cy-0h5VdB0Wx74tAJlKcKkilPWHK7tuoUWbSm6oyCUKKWFCOnLyZD6gAqAdWGVMpQ4ndv2V4PGCI4ewzI2cROrWpqy3F36U2buY2qo2oINvXK57dY9HV5URuEQHI17TFXTsvDawIs8KqraddWW2niFj4cZq5Mg2AFYw1WPoziC2W7nOsdUTQnJv2T1Cq7v8goTl8tuOF-AdxkVI9BuAVieyv_DbW9vw-boo80TfwJFC-WoMVaKBHqVRdS-zS9ToKVUpkNpB2jN9vhgMg5dPybFFbmPY8NqYIfOOInhLm3jAVCNdRjPYthGaOebjhJ5mAgASjR2uignT0qkPv6Q96RIJjWT6t2zDvSgpDx-DQB7YyKVS78H8r49_o8LcjgMFELp5JEVVa_c0ZDtJGgIzkk_DU5aa9282jaYV0fjcxcBv01HFUGlLLy9FbAQnYutgh65_ScUylCnNxGsHM0BAykr7rMP5neb6LQB69s93HYhSO3xEd1vTTi6X4mpPcFbAF856UXzQIJjUv03zU2e4uPxV_y9pQgGRkWdUsjMhM4ksO7owce1GlDyLjOsu4szRAfQVpD2vZ6F6-HnZr5_A3u1u_rWtDGMlx_j3rI-Zoa2G7o3DQbPHuQvZJMFWH2l_rqB2NA-4987Jy_lOMBCJThoTZIVdKgnLZDRMZ1geqokURxpyKJlY4R6-Kxt2I4mlG3cUuLhQUgIXqsQdTdzL35PiCVfEdf3rJgpBHzZpzACHF-klJoIMqIp5LLraq4ky7rxu3INZEJJ2EW0NhxS9c4ubJI7anhcN7bj5lXNnhc5ONH1EVTOxThOC3V6R2RlDpwuO69ulaYY85O8dVWhaxHo&uuid=94ec5735-b3cf-4e2a-a8a9-5313573e76c8&authuser=0&nonce=rsshuefdrkt4q&user=02775174769506565063&hash=3ph6d6metuejnsrdtr08nn53cahnqqgd" > mine torrent (Magnet Link)</a>

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

## TO DO
1. Train models
2. Make upscaler

   
Good luck! :)

By Alex:

> This project is possible because my boss gave me an RTX gpu, and
> allowed me to work on this project in office some time, so, i'll be
> glad if you check his website, thanks! https://fst.kz/

