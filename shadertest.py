import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    return shader

def main():
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720
# Initialize the library
    if not glfw.init():
        return
    # Set window hint NOT visible
    glfw.window_hint(glfw.VISIBLE, False)
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(DISPLAY_WIDTH, DISPLAY_HEIGHT, "hidden window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    gluPerspective(90, 0, 0.01, 12)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    vertex = create_shader(GL_VERTEX_SHADER, """
    varying vec4 uv;
    void main(){
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        uv = gl_Position;
    }""")

    fragment = create_shader(GL_FRAGMENT_SHADER, """
    varying vec4 uv;
    void main() {
        gl_FragColor = vec4(uv.x,uv.y,1,1);
    }""")

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    print(glGetProgramInfoLog(program))

    if program != -1:
        glUseProgram(program)

    glRotatef(0, 0, 0, 0) # Straight rotation
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(0, 0, 0, 0) # Rotate yaw
    glTranslatef(0, 0, -1) # Move to position
    # Draw rectangle
    
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-1, -1, 0)
    glVertex3f(-1, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(1, -1, 0)
    glEnd()
    image_buffer = glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, OpenGL.GL.GL_BGRA, OpenGL.GL.GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_HEIGHT, DISPLAY_WIDTH, 4)
    cv2.imwrite("image.png", image)
    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()