# user interaction

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
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

        # Create cube objects
        for i in range(5):
            cube = Cube()
            cube.position = [i * 2 - 4, 0, 0]
            self.objects.append(cube)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 1, 1, 1)

        for obj in self.objects:
            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()

        self.rotation += 1

    def update(self, dt):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse = [x, y]

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.select_object(x, y)

    def select_object(self, x, y):
        for obj in self.objects:
            projection_matrix = (GLdouble * 16)()
            modelview_matrix = (GLdouble * 16)()
            viewport = (GLint * 4)()

            glGetDoublev(GL_PROJECTION_MATRIX, projection_matrix)
            glGetDoublev(GL_MODELVIEW_MATRIX, modelview_matrix)
            glGetIntegerv(GL_VIEWPORT, viewport)

            winX, winY = x, viewport[3] - y
            depth = (GLdouble * 1)()
            glReadPixels(int(winX), int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, depth)

            objX, objY, objZ = gluUnProject(winX, winY, depth[0], modelview_matrix, projection_matrix, viewport)
            objX /= 100
            objY /= 100
            objZ /= 100

            if (objX >= obj.position[0] - 1 and objX <= obj.position[0] + 1 and
                    objY >= obj.position[1] - 1 and objY <= obj.position[1] + 1 and
                    objZ >= obj.position[2] - 1 and objZ <= obj.position[2] + 1):
                obj.selected = not obj.selected
                break

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Object Picking and Manipulation")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
