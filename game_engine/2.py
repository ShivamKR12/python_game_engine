import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

class PhysicsEngine:
    def __init__(self, gravity=np.array([0, -9.8, 0])):
        self.gravity = gravity
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, delta_time):
        for obj in self.objects:
            if obj.dynamic:
                obj.velocity += self.gravity * delta_time
                obj.position += obj.velocity * delta_time
                self.check_collisions(obj)

    def check_collisions(self, obj):
        for other in self.objects:
            if obj != other and self.aabb_collision(obj, other):
                self.resolve_collision(obj, other)

    def aabb_collision(self, obj1, obj2):
        for i in range(3):
            if obj1.position[i] + obj1.size[i] < obj2.position[i] - obj2.size[i] or \
               obj1.position[i] - obj1.size[i] > obj2.position[i] + obj2.size[i]:
                return False
        return True

    def resolve_collision(self, obj1, obj2):
        # Simple collision response: move obj1 back to its previous position
        for i in range(3):
            if obj1.position[i] + obj1.size[i] > obj2.position[i] - obj2.size[i] and \
               obj1.position[i] - obj1.size[i] < obj2.position[i] + obj2.size[i]:
                if obj1.velocity[i] > 0:
                    obj1.position[i] = obj2.position[i] - obj2.size[i] - obj1.size[i]
                else:
                    obj1.position[i] = obj2.position[i] + obj2.size[i] + obj1.size[i]
                obj1.velocity[i] = 0

class GameObject:
    def __init__(self, position, size, velocity, dynamic=True):
        self.position = np.array(position, dtype=float)
        self.size = np.array(size, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.dynamic = dynamic

class OBJLoader:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.load(filename)
    
    def load(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = list(map(float, parts[1:4]))
                    self.vertices.append(vertex)
                elif line.startswith('f '):
                    parts = line.strip().split()
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                    self.faces.append(face)

# Example usage:
# obj = OBJLoader('path/to/your/model.obj')
# print(obj.vertices)
# print(obj.faces)

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        self.rotation = [0, 0, 0]
        self.mouse_sensitivity = 0.1
        self.last_mouse_pos = pygame.mouse.get_pos()

        self.physics_engine = PhysicsEngine()
        self.cube1 = GameObject([0, 0, 0], [1, 1, 1], [0, 0, 0])
        self.cube2 = GameObject([2, 0, 0], [1, 1, 1], [0, 0, 0], dynamic=False)
        self.physics_engine.add_object(self.cube1)
        self.physics_engine.add_object(self.cube2)
        
        self.obj_model = OBJLoader('block.obj')
        
        self.texture_id = self.load_texture("texture.png")
        self.init_lighting()
    
    def init_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 1, 1, 1])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
        glMaterialf(GL_FRONT, GL_SHININESS, 50)

    def load_texture(self, texture_file):
        texture_surface = pygame.image.load(texture_file)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
        width, height = texture_surface.get_rect().size
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        return texture_id
    
    def draw_obj_model(self):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLES)
        for face in self.obj_model.faces:
            for vertex in face:
                glVertex3fv(self.obj_model.vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


    def draw_cube():
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rotation[1] -= 1
        if keys[K_RIGHT]:
            self.rotation[1] += 1
        if keys[K_UP]:
            self.rotation[0] -= 1
        if keys[K_DOWN]:
            self.rotation[0] += 1

        mouse_pos = pygame.mouse.get_pos()
        dx, dy = mouse_pos[0] - self.last_mouse_pos[0], mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos

        self.rotation[1] += dx * self.mouse_sensitivity
        self.rotation[0] -= dy * self.mouse_sensitivity

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        delta_time = 0.01
        self.physics_engine.update(delta_time)
        
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube(self.cube1)
        self.draw_cube(self.cube2)
        self.draw_obj_model()
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.handle_input()
            self.update()
        pygame.quit()

if __name__ == "__main__":
    engine = GameEngine(800, 600)
    engine.run()