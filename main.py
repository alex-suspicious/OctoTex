import time
import tkinter
from tkinter import ttk, PhotoImage
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import pygame

from pyopengltk import OpenGLFrame
from tkinter.messagebox import showinfo
import os


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

		void main()
		{
			vec3 lightColor = vec3(1,1,1);

			float ambientStrength = 1;
			vec3 ambient = ambientStrength * lightColor;

			vec4 diffuseMap = texture2D(texture0, uv0.xy);
			float alpha = diffuseMap.a;

			vec4 normalMap = texture2D(texture1, uv0.xy);
			vec4 roughnessMap = texture2D(texture2, uv0.xy);

			float dist = dot(vec3(3,0,3), normalMap.xyz);
			//dist *= (1-roughnessMap.x);

			//vec3 reflectedDirection = reflect(normalize(ws_coords), normal);
			//vec4 cubeMap = texture(uniform_ReflectionTexture, reflectedDirection).xyz

			vec3 finalColor = diffuseMap.xyz * ambient.xyz;

		    color.xyz = ( finalColor * dist );
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

		self.start = time.time()
		self.nframes = 0

	def loadNewTexture(self, path):
		self.diffuse = loadTexture(path)
		self.normals = loadTexture(path.replace("upscaled","normals").replace(".png","_normal.png"))
		self.roughness = loadTexture(path.replace("upscaled","roughness").replace(".png","_rough.png"))

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

		
		glTranslatef(0, 0, -1.6)

		if self.program != -1:
			glUseProgram(self.program)
		#glRotatef(self.nframes*0.5, 0, 1, 0)

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
		print("fps",self.nframes / tm, end="\r" )


if __name__ == '__main__':
	Upscaled = os.listdir("textures/processing/upscaled/")

	root = tkinter.Tk()
	root.title('OctoTex')
	root.geometry('1280x720')
	root.rowconfigure(0, weight=1)
	app = AppOgl(root, width=320, height=200)

	def item_selected(event):
		for selected_item in tree.selection():
			item = tree.item(selected_item)
			record = item['values']

			app.loadNewTexture(f"textures/processing/upscaled/{record[0]}")



	upscaledFrame = tkinter.Frame(root, background="pink")
	upscaledFrame.pack(fill=tkinter.Y, side=tkinter.LEFT)  # Expand in both directions

	columns = ('name')

	tree = ttk.Treeview(upscaledFrame, columns=columns, show='headings')
	tree.heading('name', text='textures')


	# add data to the treeview
	for x in range(len(Upscaled)):
		temp = Upscaled[x]
		#icon = PhotoImage(file=f"textures/processing/upscaled/{temp}")
		tree.insert('', tkinter.END, values=(temp))

	tree.bind('<<TreeviewSelect>>', item_selected)
	tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)  # Expand and fill in both directions

	scrollbar = ttk.Scrollbar(upscaledFrame, orient=tkinter.VERTICAL, command=tree.yview)
	tree.configure(yscroll=scrollbar.set)
	scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # Place Scrollbar to the right

	

	app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
	app.animate = 1
	app.after(100, app.printContext)

	root.mainloop()
