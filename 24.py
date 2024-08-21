import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

# Define vertex data for a cube
cube_vertices = [
    (-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1),  # Front face
    (-1, -1, -1), (-1,  1, -1), ( 1,  1, -1), ( 1, -1, -1),  # Back face
    (-1,  1, -1), (-1,  1,  1), ( 1,  1,  1), ( 1,  1, -1),  # Top face
    (-1, -1, -1), ( 1, -1, -1), ( 1, -1,  1), (-1, -1,  1),  # Bottom face
    ( 1, -1, -1), ( 1,  1, -1), ( 1,  1,  1), ( 1, -1,  1),  # Right face
    (-1, -1, -1), (-1, -1,  1), (-1,  1,  1), (-1,  1, -1)   # Left face
]

# Define vertex indices for drawing the cube
cube_indices = [
    0,  1,  2,  0,  2,  3,  # Front face
    4,  5,  6,  4,  6,  7,  # Back face
    8,  9, 10,  8, 10, 11,  # Top face
   12, 13, 14, 12, 14, 15,  # Bottom face
   16, 17, 18, 16, 18, 19,  # Right face
   20, 21, 22, 20, 22, 23   # Left face
]

# Define normal vectors for each face of the cube
cube_normals = [
    ( 0,  0,  1), ( 0,  0, -1), ( 0,  1,  0),  # Front, Back, Top
    ( 0, -1,  0), ( 1,  0,  0), (-1,  0,  0)   # Bottom, Right, Left
]

class Cube:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        # Flatten vertex and normal data
        flat_cube_vertices = [vertex for face_vertices in cube_vertices for vertex in face_vertices]
        flat_cube_normals = [normal for face_normals in cube_normals for normal in face_normals]

        # Use the flattened data
        self.vertices = self.batch.add_indexed(36, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', flat_cube_vertices),
                                               ('n3f/static', flat_cube_normals))
        self.position = [0, 0, 0]
        self.selected = False

    def draw(self):
        if self.selected:
            glColor3f(1, 0, 0)  # Selected color (red)
        else:
            glColor3f(1, 1, 1)  # Default color (white)
        self.batch.draw()


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Setup initial camera position
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = -5

        # Setup rotation angle
        self.rotation = 0

        # Setup input handling
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.mouse = [0, 0]
        self.objects = []

        # Create cube objects
        for i in range(5):
            cube = Cube()
            cube.position = [i * 2 - 4, 0, 0]
            self.objects.append(cube)

        # Create framebuffer object (FBO)
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Create texture to render to
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture, 0)

        # Create renderbuffer for depth and stencil attachment
        self.depth_stencil_rb = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_stencil_rb)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.depth_stencil_rb)

        # Check framebuffer completeness
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Framebuffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_stencil_rb)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)

    def on_draw(self):
        # Bind the framebuffer object (FBO) to render to the texture
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)

        self.clear()

        glLoadIdentity()
        glRotatef(self.rotation, 0, 1, 0)
        glTranslatef(0, 0, -5)

        for obj in self.objects:
            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()

        # Unbind the framebuffer object (FBO)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Render the texture to the screen
        glViewport(0, 0, self.width, self.height)
        self.clear()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)
        glTexCoord2f(0, 1)
        glVertex2f(0, self.height)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def update(self, dt):
        self.rotation += 1

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Render to Texture with OpenGL")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
