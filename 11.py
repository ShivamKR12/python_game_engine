# scene graph structure

import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

class Node:
    def __init__(self):
        self.children = []
        self.parent = None
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def update(self, dt):
        pass

    def draw(self):
        for child in self.children:
            child.draw()

class TransformNode(Node):
    def __init__(self):
        super().__init__()
        self.matrix = np.identity(4, dtype=np.float32)

    def update_matrix(self):
        translation_matrix = np.identity(4, dtype=np.float32)
        translation_matrix[:3, 3] = self.translation

        rotation_matrix_x = np.identity(4, dtype=np.float32)
        rotation_matrix_x[:3, :3] = np.array([
            [1, 0, 0],
            [0, np.cos(np.radians(self.rotation[0])), -np.sin(np.radians(self.rotation[0]))],
            [0, np.sin(np.radians(self.rotation[0])), np.cos(np.radians(self.rotation[0]))]
        ])

        rotation_matrix_y = np.identity(4, dtype=np.float32)
        rotation_matrix_y[:3, :3] = np.array([
            [np.cos(np.radians(self.rotation[1])), 0, np.sin(np.radians(self.rotation[1]))],
            [0, 1, 0],
            [-np.sin(np.radians(self.rotation[1])), 0, np.cos(np.radians(self.rotation[1]))]
        ])

        rotation_matrix_z = np.identity(4, dtype=np.float32)
        rotation_matrix_z[:3, :3] = np.array([
            [np.cos(np.radians(self.rotation[2])), -np.sin(np.radians(self.rotation[2])), 0],
            [np.sin(np.radians(self.rotation[2])), np.cos(np.radians(self.rotation[2])), 0],
            [0, 0, 1]
        ])

        scale_matrix = np.identity(4, dtype=np.float32)
        scale_matrix[:3, :3] = np.diag(self.scale)

        self.matrix = np.dot(translation_matrix, np.dot(rotation_matrix_x, np.dot(rotation_matrix_y,
                                                                                   np.dot(rotation_matrix_z,
                                                                                          scale_matrix))))

    def update(self, dt):
        self.update_matrix()
        for child in self.children:
            child.update(dt)

    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.matrix)
        for child in self.children:
            child.draw()
        glPopMatrix()

class Cube:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(24, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', cube_vertices),
                                               ('n3f/static', cube_normals))

    def draw(self):
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

        # Create scene graph
        self.root_node = TransformNode()
        self.cube_node = TransformNode()
        self.cube = Cube()
        self.cube_node.add_child(self.cube)
        self.root_node.add_child(self.cube_node)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 1, 1, 1)

        # Update and draw the scene graph
        self.root_node.update(0)
        self.root_node.draw()

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
    window = GameWindow(width=800, height=600, caption="Scene Graph Example")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
