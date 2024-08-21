# optimized rendering

import pyglet
from pyglet.gl import *
from pyglet.window import key

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
        self.vertices = self.batch.add_indexed(24, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', cube_vertices),
                                               ('n3f/static', cube_normals))

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

        # Load texture
        self.texture = pyglet.image.load("texture.png").get_texture()

        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (-1, 1, 1, 0))  # Set position of light source
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))   # Set diffuse color of light

        # Setup VBO for cube rendering
        self.cube_vbo = self.create_vbo()

    def create_vbo(self):
        vertex_data = []
        for i, vertex in enumerate(cube_vertices):
            vertex_data.extend(vertex)
            vertex_data.extend(cube_normals[i])
        vbo_id = GLuint()
        glGenBuffers(1, vbo_id)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
        glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, (GLfloat * len(vertex_data))(*vertex_data), GL_STATIC_DRAW)
        return vbo_id

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 1, 1, 1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

        # Draw the cube using VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.cube_vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, None)
        glNormalPointer(GL_FLOAT, 24, ctypes.c_void_p(12))
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        glDisable(GL_TEXTURE_2D)

        self.rotation += 1

    def update(self, dt):
        if self.keys[key.LEFT]:
            self.camera_x -= 0.1
        if self.keys[key.RIGHT]:
            self.camera_x += 0.1
        if self.keys[key.UP]:
            self.camera_y += 0.1
        if self.keys[key.DOWN]:
            self.camera_y -= 0.1

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Simple 3D Game Engine")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    window.cube = Cube()
    pyglet.app.run()
