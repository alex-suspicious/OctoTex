import time
import tkinter
from tkinter import ttk, PhotoImage, Menu, messagebox
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import pygame
import pathlib
import sys

from pyopengltk import OpenGLFrame
from tkinter.messagebox import showinfo
import os

import load as loader
import upscale as upscaler
import pbr as materializer
import write as writer
import config
from tqdm import tqdm

from zipfile import ZipFile

from ai.PBR.model import Unet
import ai.PBR.eval_disp as displacements
import ai.PBR.eval_norm as normals
import ai.PBR.eval_rough as roughness
sys.path
sys.path.append('./nvidia')
from octahedral import *

mouse_pressed = False
mouse_coord = [0,0]
mouse_prev_coord = [0,0]

pitch = 0
yaw = 0

temp_pitch = 0
temp_yaw = 0

print("Use webui instead!")
exit()

def loadTexturesTkinter():
	loadDirId = 0
	loadDir = "captures"

	mods = [f for f in pathlib.Path().glob(f"{config.rtx_remix_dir}/mods/*")]
	if( len(mods) > 0 ):
		print("Directories for importing: ")

		print("0 | captures")
		for x in range(len(mods)):
			mod_path = str(mods[x]).replace(f"{config.rtx_remix_dir}/mods/","")
			print(f"{x+1} | {mod_path}")


		#loadDirId = int(input("From what dir you want to load the textures, select by index: "))
		loadDirId = 0
		loadDirId -= 1
		if( loadDirId != -1 ):
			loadDir = str(mods[loadDirId]).replace(f"{config.rtx_remix_dir}/","") + "/SubUSDs/textures/diffuse"
		else:
			loadDir += "/textures"
	else:
		loadDir += "/textures"

	def endLoading( files ):
		messagebox.showinfo("Loader", f"Loading is done!\n{files} textures was loaded.")
		updateTextureTree()

	loader.loadTextures(loadDir,0,0,endLoading)

def aiGenerateDisplacements():
	messagebox.showinfo("AI", f"Normal map generation may take some time.\nPlease check the console for the generation status.\nPress OK if you understand everything.")

	import gc
	import torch
	torch.cuda.empty_cache()
	gc.collect()

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	PATH_CHK = "ai/PBR/checkpoints/disp/disp_net_last.pth"

	norm_net = Unet().to(device)
	checkpoint = torch.load(PATH_CHK)
	norm_net.load_state_dict(checkpoint["model"])

	displacements.generateDisp(norm_net,"textures/processing/upscaled","textures/processing/displacements")
	messagebox.showinfo("AI", f"Normal map generation is done!")
	updateTextureTree()

def aiGenerateRoughness():
	messagebox.showinfo("AI", f"Rough map generation may take some time.\nPlease check the console for the generation status.\nPress OK if you understand everything.")

	import gc
	import torch
	torch.cuda.empty_cache()
	gc.collect()

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	PATH_CHK = "ai/PBR/checkpoints/rough/rough_net_last.pth"

	norm_net = Unet().to(device)
	checkpoint = torch.load(PATH_CHK)
	norm_net.load_state_dict(checkpoint["model"])

	roughness.generateRough(norm_net,"textures/processing/upscaled","textures/processing/roughness")
	messagebox.showinfo("AI", f"Rough map generation is done!")
	updateTextureTree()

def aiGenerateNormals():
	messagebox.showinfo("AI", f"Normal map generation may take some time.\nPlease check the console for the generation status.\nPress OK if you understand everything.")

	import gc
	import torch
	torch.cuda.empty_cache()
	gc.collect()

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	PATH_CHK = "ai/PBR/checkpoints/norm/norm_net_last.pth"

	norm_net = Unet().to(device)
	checkpoint = torch.load(PATH_CHK)
	norm_net.load_state_dict(checkpoint["model"])

	normals.generateNorm(norm_net,"textures/processing/upscaled","textures/processing/normaldx")
	for x in tqdm( os.listdir(f"textures/processing/normaldx/"), desc="Generating..." ):
		if x.endswith(".png"):
			LightspeedOctahedralConverter.convert_dx_file_to_octahedral(f"textures/processing/normaldx/{x}", f"textures/processing/normals/{x}")

	messagebox.showinfo("AI", f"Normal map generation is done!")
	updateTextureTree()

def upscaleTexturesTkinter():
	messagebox.showinfo("Upscaler x4", f"Upscaling may take some time.\nPlease check the console for the upscaling status.\nPress OK if you understand everything.")
	upscaler.upscaleTextures()

	messagebox.showinfo("Upscaler x4", f"Upscaling is done!")
	updateTextureTree()

def upscale2xTexturesTkinter():
	messagebox.showinfo("Upscaler x8", f"Upscaling may take some time.\nPlease check the console for the upscaling status.\nPress OK if you understand everything.")
	upscaler.upscaleTextures2X()

	messagebox.showinfo("Upscaler x8", f"Upscaling is done!")
	updateTextureTree()

def materializeTexturesTkinter():
	messagebox.showinfo("Materializer", f"PBR generation may take some time.\nPlease check the console for the generation status.\nPress OK if you understand everything.")
	materializer.generatePBR()

	messagebox.showinfo("Materializer", f"PBR generation is done!")
	updateTextureTree()

def writeTexturesBack():
	mod_dir = "OctoTexGUI"
	isExist = os.path.exists(f"{config.rtx_remix_dir}/mods/{mod_dir}")
	if not isExist:
		with ZipFile("mods/modTemplate.zip", 'r') as zObject:
			zObject.extractall( path=f"{config.rtx_remix_dir}/mods/")

		os.rename(f"{config.rtx_remix_dir}/mods/modTemplate", f"{config.rtx_remix_dir}/mods/{mod_dir}")

	replacements_file = "replacements.usda"
	writer.saveAllTextures(mod_dir, replacements_file)
	messagebox.showinfo("Writer", f"All textures has been written back!")

def OnMouseDown(event):
	global mouse_pressed
	mouse_pressed = True

def OnMouseUp(event):
	global mouse_pressed
	mouse_pressed = False
	
def motion(event):
	global pitch, temp_pitch, yaw, temp_yaw, mouse_pressed, mouse_prev_coord, mouse_coord
	x, y = event.x, event.y
	
	mouse_coord = [x,y]
	if( not mouse_pressed ):
		mouse_prev_coord = [x,y]
		temp_pitch = pitch
		temp_yaw = yaw
	else:
		yaw = temp_yaw + (mouse_coord[0]-mouse_prev_coord[0])*0.3
		pitch = temp_pitch + (mouse_coord[1]-mouse_prev_coord[1])*0.3

	#print(yaw)

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    return shader

def loadTexture(path):
    textureSurface = pygame.image.load(path)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texid


class AppOgl(OpenGLFrame):

	def initgl(self):
		GL.glViewport(0, 0, self.width, self.height)
		GL.glClearColor(0.0, 0.0, 0.0, 0.0)    

		
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)

		vertex = create_shader(GL_VERTEX_SHADER, """
		varying vec2 uv0;
		varying vec3 normal;
		varying vec4 lamp;

		void main(){
		    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
		    gl_TexCoord[0] = gl_MultiTexCoord0;
		    uv0 = gl_MultiTexCoord0;
		    normal = normalize(gl_NormalMatrix * gl_Normal);

		    lamp = vec4(0.5,0,1,0) * gl_ModelViewProjectionMatrix;
		}""")

		fragment = create_shader(GL_FRAGMENT_SHADER, """
		#version 330 core

		varying vec2 uv0;
		varying vec3 normal;
		varying vec4 lamp;
		

		out vec4 color;

		uniform sampler2D texture0;
		uniform sampler2D texture1;
		uniform sampler2D texture2;
		uniform samplerCube uniform_ReflectionTexture;
		uniform float time;

		void main()
		{
			vec3 lightColor = vec3(1,1,1);

			float ambientStrength = 1;
			vec3 ambient = ambientStrength * lightColor;

			vec4 diffuseMap = texture2D(texture0, uv0.xy);
			float alpha = diffuseMap.a;

			vec4 normalMap = texture2D(texture1, uv0.xy);
			vec4 roughnessMap = texture2D(texture2, uv0.xy);

			//float dist = dot(vec3(3,0,3), normalMap.xyz);
			//dist *= (1-roughnessMap.x);

			//vec3 reflectedDirection = reflect(normalize(ws_coords), normal);
			//vec4 cubeMap = texture(uniform_ReflectionTexture, reflectedDirection).xyz

			vec3 finalColor = diffuseMap.xyz;
			finalColor += clamp(cos(uv0.x*5 + time + normalMap.r),-1,1)*abs(1-roughnessMap.r);

		    color.xyz = ( finalColor );
		    color.a = alpha;
		}""")

		self.program = glCreateProgram()
		glAttachShader(self.program, vertex)
		glAttachShader(self.program, fragment)
		glLinkProgram(self.program)
		print(glGetProgramInfoLog(self.program))

		self.diffuse = loadTexture("textures/logo.png")
		self.normals = loadTexture("textures/logo.png")
		self.roughness = loadTexture("textures/logo.png")
		self.time_location = time_location = glGetUniformLocation(self.program, "time")

		self.start = time.time()
		self.nframes = 0

	def loadNewTexture(self, path):
		self.diffuse = loadTexture(path)
		self.normals = loadTexture(path.split("/")[-1].replace("upscaled","normals").replace(".png","_normal.png"))
		self.roughness = loadTexture(path.split("/")[-1].replace("upscaled","roughness").replace(".png","_rough.png"))

		texture0 = glGetUniformLocation(self.program, "texture0")
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.diffuse)
		glUniform1i(texture0, 0)


		texture1 = glGetUniformLocation(self.program, "texture1")
		glActiveTexture(GL_TEXTURE1)
		glBindTexture(GL_TEXTURE_2D, self.normals)
		glUniform1i(texture1, 1)


		texture2 = glGetUniformLocation(self.program, "texture2")
		glActiveTexture(GL_TEXTURE2)
		glBindTexture(GL_TEXTURE_2D, self.roughness)
		glUniform1i(texture2, 2)


	def redraw(self):
		glLoadIdentity()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		gluPerspective(70, self.width/self.height, 0.1, 200)

		
		glTranslatef(0, 0, -2.8)

		if self.program != -1:
			glUseProgram(self.program)

		glRotatef(yaw, 0, 1, 0)
		glRotatef(pitch, 1, 0, 0)

		glBegin(GL_QUADS)
		glColor3f(1, 1, 1)

		glTexCoord2f(0, 0)
		glVertex3f(-1, -1, 0)

		glTexCoord2f(0, 1)
		glVertex3f(-1, 1, 0)
		
		glTexCoord2f(1, 1)
		glVertex3f(1, 1, 0)

		glTexCoord2f(1, 0)
		glVertex3f(1, -1, 0)
		glEnd()


		tm = time.time() - self.start
		self.nframes += 1
		glUniform1f(self.time_location, self.nframes*0.01)

		#print("fps",self.nframes / tm, end="\r" )

if __name__ == '__main__':
	root = tkinter.Tk()
	root.title('OctoTex')
	root.geometry('1280x720')
	root.rowconfigure(0, weight=1)
	app = AppOgl(root, width=320, height=200)


	menubar = Menu(root)
	root.config(menu=menubar)
	file_menu = Menu(menubar)
	file_menu.add_command(
	    label='Load',
	    command=loadTexturesTkinter
	)

	file_menu.add_command(
	    label='Write',
	    command=writeTexturesBack
	)

	menubar.add_cascade(
	    label="Data",
	    menu=file_menu
	)

	root.config(menu=menubar)
	file_menu = Menu(menubar)

	file_menu.add_command(
	    label='Generate PBR',
	    command=materializeTexturesTkinter
	)

	menubar.add_cascade(
	    label="Algorithms",
	    menu=file_menu
	)


	root.config(menu=menubar)
	file_menu = Menu(menubar)

	file_menu.add_command(
	    label='Upscale x4',
	    command=upscaleTexturesTkinter
	)

	file_menu.add_command(
	    label='Upscale x8',
	    command=upscale2xTexturesTkinter
	)

	file_menu.add_command(
	    label='Generate normal maps',
	    command=aiGenerateNormals
	)

	file_menu.add_command(
	    label='Generate rough maps',
	    command=aiGenerateRoughness
	)

	file_menu.add_command(
	    label='Generate displacement maps',
	    command=aiGenerateDisplacements
	)

	menubar.add_cascade(
	    label="AI",
	    menu=file_menu
	)


	root.bind('<Motion>', motion)
	root.bind("<ButtonPress-1>", OnMouseDown)
	root.bind("<ButtonRelease-1>", OnMouseUp)

	def item_selected(event):
		for selected_item in tree.selection():
			item = tree.item(selected_item)
			record = item['values']

			app.loadNewTexture(record[1])



	upscaledFrame = tkinter.Frame(root, background="pink")
	upscaledFrame.pack(fill=tkinter.Y, side=tkinter.LEFT)  # Expand in both directions

	columns = ('name')

	tree = ttk.Treeview(upscaledFrame, columns=columns, show='headings')
	tree.heading('name', text='textures')

	def updateTextureTree():
		Upscaled = os.listdir("textures/processing/upscaled/")
		Diffuse = os.listdir("textures/processing/diffuse/")

		
		alreadyWas = []
		#tree.delete()

		for item in tree.get_children():
			tree.delete(item)

		# add data to the treeview
		for x in range(len(Upscaled)):
			temp = Upscaled[x]
			#icon = PhotoImage(file=f"textures/processing/upscaled/{temp}")
			tree.insert('', tkinter.END, values=(temp,f"textures/processing/upscaled/{temp}"))
			alreadyWas.append(temp)

		for x in range(len(Diffuse)):
			temp = Diffuse[x]
			if( temp in alreadyWas ):
				continue
			#icon = PhotoImage(file=f"textures/processing/upscaled/{temp}")
			tree.insert('', tkinter.END, values=(temp,f"textures/processing/diffuse/{temp}"))

	updateTextureTree()

	tree.bind('<<TreeviewSelect>>', item_selected)
	tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)  # Expand and fill in both directions

	scrollbar = ttk.Scrollbar(upscaledFrame, orient=tkinter.VERTICAL, command=tree.yview)
	tree.configure(yscroll=scrollbar.set)
	scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # Place Scrollbar to the right


	app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
	app.animate = 1
	app.after(100, app.printContext)

	root.mainloop()
