import ai.ESRGAN.upscaler
import ai.RealESRGAN.upscaler
import config

if( "Real" in config.upscale_model ):
	ai.RealESRGAN.upscaler.upscaleAll()
else:
	ai.ESRGAN.upscaler.upscaleAll()