import pyglet
from pyglet.gl import *

# Define vertex data for a cube
cube_vertices = [
    # Front face
    (-1, -1,  1),
    ( 1, -1,  1),
    ( 1,  1,  1),
    (-1,  1,  1),
    # Back face
    (-1, -1, -1),
    (-1,  1, -1),
    ( 1,  1, -1),
    ( 1, -1, -1),
    # Top face
    (-1,  1, -1),
    (-1,  1,  1),
    ( 1,  1,  1),
    ( 1,  1, -1),
    # Bottom face
    (-1, -1, -1),
    ( 1, -1, -1),
    ( 1, -1,  1),
    (-1, -1,  1),
    # Right face
    ( 1, -1, -1),
    ( 1,  1, -1),
    ( 1,  1,  1),
    ( 1, -1,  1),
    # Left face
    (-1, -1, -1),
    (-1, -1,  1),
    (-1,  1,  1),
    (-1,  1, -1)
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

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Setup projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # Setup initial camera position
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        # Setup rotation angle
        self.rotation = 0

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glRotatef(self.rotation, 1, 1, 1)

        # Draw the cube
        glBegin(GL_TRIANGLES)
        for i in range(0, len(cube_indices), 3):
            for j in range(3):
                glVertex3fv(cube_vertices[cube_indices[i + j]])
        glEnd()

        self.rotation += 1

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Simple 3D Game Engine")
    pyglet.app.run()
