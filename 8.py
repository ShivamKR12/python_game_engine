# scene complexisity

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

# Define texture coordinates for the cube
cube_tex_coords = [
    (0, 0), (1, 0), (1, 1), (0, 1),  # Front face
    (0, 0), (1, 0), (1, 1), (0, 1),  # Back face
    (0, 0), (1, 0), (1, 1), (0, 1),  # Top face
    (0, 0), (1, 0), (1, 1), (0, 1),  # Bottom face
    (0, 0), (1, 0), (1, 1), (0, 1),  # Right face
    (0, 0), (1, 0), (1, 1), (0, 1)   # Left face
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

# Define vertex data for a quad
quad_vertices = [
    (-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)
]

# Define texture coordinates for the quad
quad_tex_coords = [
    (0, 0), (1, 0), (1, 1), (0, 1)
]

# Define vertex indices for drawing the quad
quad_indices = [0, 1, 2, 0, 2, 3]

class Cube:
    def __init__(self, texture):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(24, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', cube_vertices),
                                               ('t2f/static', cube_tex_coords),
                                               ('n3f/static', cube_normals))
        self.texture = texture

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        self.batch.draw()
        glDisable(GL_TEXTURE_2D)

class Quad:
    def __init__(self, texture):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(4, GL_QUADS, None, quad_indices,
                                               ('v3f/static', quad_vertices),
                                               ('t2f/static', quad_tex_coords))
        self.texture = texture

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        self.batch.draw()
        glDisable(GL_TEXTURE_2D)

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

        # Load textures
        self.cube_texture = pyglet.image.load("cube_texture.png").get_texture()
        self.quad_texture = pyglet.image.load("quad_texture.png").get_texture()

        # Create objects
        self.cube = Cube(self.cube_texture)
        self.quad = Quad(self.quad_texture)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 1, 1, 1)

        # Draw objects
        self.cube.draw()
        self.quad.draw()

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
    window = GameWindow(width=800, height=600, caption="Complex 3D Scene")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
