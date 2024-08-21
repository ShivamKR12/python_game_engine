# level of detail

import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

# Define vertex data for a simplified cube (lower LOD)
simplified_cube_vertices = [
    (-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1),  # Front face
    (-1, -1, -1), (-1,  1, -1), ( 1,  1, -1), ( 1, -1, -1)   # Back face
]

# Define vertex indices for drawing the simplified cube
simplified_cube_indices = [
    0,  1,  2,  0,  2,  3,  # Front face
    4,  5,  6,  4,  6,  7   # Back face
]

# Define normal vectors for each face of the simplified cube
simplified_cube_normals = [
    ( 0,  0,  1), ( 0,  0, -1), ( 0,  1,  0),  # Front, Back, Top
    ( 0, -1,  0)   # Bottom
]

class LODCube:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(8, GL_TRIANGLES, None, simplified_cube_indices,
                                               ('v3f/static', simplified_cube_vertices),
                                               ('n3f/static', simplified_cube_normals))

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
        self.lod_cube = LODCube()

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 1, 1, 1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

        # Calculate view frustum planes
        proj_matrix = (GLdouble * 16)()
        glGetDoublev(GL_PROJECTION_MATRIX, proj_matrix)
        modelview_matrix = (GLdouble * 16)()
        glGetDoublev(GL_MODELVIEW_MATRIX, modelview_matrix)
        clip_matrix = np.dot(np.array(proj_matrix).reshape(4, 4), np.array(modelview_matrix).reshape(4, 4))
        frustum_planes = [
            (clip_matrix[3] + clip_matrix[0]),  # Left
            (clip_matrix[3] - clip_matrix[0]),  # Right
            (clip_matrix[3] + clip_matrix[1]),  # Bottom
            (clip_matrix[3] - clip_matrix[1]),  # Top
            (clip_matrix[3] + clip_matrix[2]),  # Near
            (clip_matrix[3] - clip_matrix[2]),  # Far
        ]

        # Check if the cube is inside the view frustum
        if self.is_cube_in_frustum(frustum_planes):
            self.render_cube()
        else:
            self.render_simplified_cube()

        glDisable(GL_TEXTURE_2D)

        self.rotation += 1

    def is_cube_in_frustum(self, planes):
        for vertex in simplified_cube_vertices:
            for plane in planes:
                if np.dot(plane[:3], vertex) + plane[3] <= 0:
                    return False
        return True

    def render_cube(self):
        # Draw the detailed cube
        self.lod_cube.batch.draw()

    def render_simplified_cube(self):
        # Draw the simplified cube
        glPushMatrix()
        glScalef(0.5, 0.5, 0.5)  # Adjust scale for the simplified cube
        self.lod_cube.batch.draw()
        glPopMatrix()

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
    pyglet.app.run()
