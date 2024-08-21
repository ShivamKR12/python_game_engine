# loading and rendering complex 3D models

import pyglet
from pyglet.gl import *
from pyglet.window import key
from pywavefront import Wavefront

class Model:
    def __init__(self, obj_file):
        self.batch = pyglet.graphics.Batch()
        self.obj = Wavefront(obj_file)
        self.groups = []
        self.vertices = []

        # Extract vertices and groups
        for name, material in self.obj.materials.items():
            vertex_list = self.batch.add(len(material.vertices) // 3, GL_TRIANGLES, material,
                                         ('v3f/static', material.vertices), ('n3f/static', material.normals),
                                         ('t2f/static', material.texcoords))
            self.groups.append((material, vertex_list))
            self.vertices.extend(material.vertices)

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

        # Load 3D model
        self.model = Model("model.obj")

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        glRotatef(self.rotation, 0, 1, 0)

        # Draw the model
        self.model.draw()

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
    window = GameWindow(width=800, height=600, caption="3D Model Rendering")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
