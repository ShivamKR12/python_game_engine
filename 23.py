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

# Generate noise texture for SSAO
def generate_noise_texture():
    noise = np.random.rand(4, 4, 3) * 2.0 - 1.0
    noise_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, noise_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 4, 4, 0, GL_RGB, GL_FLOAT, noise)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBindTexture(GL_TEXTURE_2D, 0)
    return noise_texture

class Cube:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(24, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', cube_vertices),
                                               ('n3f/static', cube_normals))
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

        # Generate noise texture for SSAO
        self.noise_texture = generate_noise_texture()

        # Create cube objects
        for i in range(5):
            cube = Cube()
            cube.position = [i * 2 - 4, 0, 0]
            self.objects.append(cube)

    def on_draw(self):
        self.clear()

        glLoadIdentity()
        glRotatef(self.rotation, 0, 1, 0)
        glTranslatef(0, 0, -5)

        glBindTexture(GL_TEXTURE_2D, self.noise_texture)
        for obj in self.objects:
            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()

    def update(self, dt):
        self.rotation += 1

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Ambient Occlusion with OpenGL")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
