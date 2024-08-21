import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Add rendering logic here
    
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
###################################################################
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Define vertices and edges of a cube
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

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
################################################################
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class GameEngine:
    def __init__(self, width, height):
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.display = (width, height)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        
        # Set up perspective
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        # Initialize rotation angles
        self.rotation = [0, 0, 0]
        
        # Define vertices and edges of a cube
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
    
    def draw_cube(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
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

    def update(self):
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube()
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
########################################################################
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        self.rotation = [0, 0, 0]
        
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
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
    
    def draw_cube(self):
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
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

    def update(self):
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube()
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
######################################################################
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        self.rotation = [0, 0, 0]
        
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        self.surfaces = [
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (6, 5, 1, 2),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (3, 0, 4, 7)
        ]
        
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
    
    def draw_cube(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glTexCoord2f(vertex % 2, vertex // 2)
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
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

    def update(self):
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube()
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
###################################################################
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

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
        
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        self.surfaces = [
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (6, 5, 1, 2),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (3, 0, 4, 7)
        ]
        
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
    
    def draw_cube(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glTexCoord2f(vertex % 2, vertex // 2)
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
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

        # Handle mouse movement
        mouse_pos = pygame.mouse.get_pos()
        dx, dy = mouse_pos[0] - self.last_mouse_pos[0], mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos

        self.rotation[1] += dx * self.mouse_sensitivity
        self.rotation[0] -= dy * self.mouse_sensitivity

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube()
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
#########################################################################
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
        if obj.position[1] < -1:  # Simple ground collision
            obj.position[1] = -1
            obj.velocity[1] = 0

class GameObject:
    def __init__(self, position, velocity, dynamic=True):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.dynamic = dynamic

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
        self.cube = GameObject([0, 0, 0], [0, 0, 0])
        self.physics_engine.add_object(self.cube)
        
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        self.surfaces = [
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (6, 5, 1, 2),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (3, 0, 4, 7)
        ]
        
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
    
    def draw_cube(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glTexCoord2f(vertex % 2, vertex // 2)
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
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
        glTranslatef(*self.cube.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        self.draw_cube()
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
##########################################################
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
        
        self.vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        self.surfaces = [
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (6, 5, 1, 2),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (3, 0, 4, 7)
        ]
        
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
    
    def draw_cube(self, obj):
        glPushMatrix()
        glTranslatef(*obj.position)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glTexCoord2f(vertex % 2, vertex // 2)
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glPopMatrix()
        
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
##############################################################
import os

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
        
        self.obj_model = OBJLoader('path/to/your/model.obj')
        
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
###########################################################
class PhysicsEngine:
    def __init__(self, gravity=np.array([0, -9.8, 0]), friction=0.9, restitution=0.8):
        self.gravity = gravity
        self.friction = friction
        self.restitution = restitution
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
        # Simple collision response: apply restitution and friction
        for i in range(3):
            if obj1.position[i] + obj1.size[i] > obj2.position[i] - obj2.size[i] and \
               obj1.position[i] - obj1.size[i] < obj2.position[i] + obj2.size[i]:
                if obj1.velocity[i] > 0:
                    obj1.position[i] = obj2.position[i] - obj2.size[i] - obj1.size[i]
                else:
                    obj1.position[i] = obj2.position[i] + obj2.size[i] + obj1.size[i]
                obj1.velocity[i] *= -self.restitution
                obj1.velocity *= self.friction

class GameObject:
    def __init__(self, position, size, velocity, dynamic=True):
        self.position = np.array(position, dtype=float)
        self.size = np.array(size, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.dynamic = dynamic

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
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
        
        self.obj_model = OBJLoader('path/to/your/model.obj')
        
        self.texture_id = self.load_texture("texture.png")
        self.init_lighting()

        self.font = pygame.font.SysFont('Arial', 18)
    
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

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
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
        
        self.render_text(f'Cube Position: {self.cube1.position}', (10, 10))
        
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
##############################################################
class Button:
    def __init__(self, text, position, size, font, color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.rect = pygame.Rect(position, size)
        self.rendered_text = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_rect = self.rendered_text.get_rect(center=self.rect.center)
        screen.blit(self.rendered_text, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Example usage:
# font = pygame.font.SysFont('Arial', 24)
# button = Button('Start', (50, 50), (100, 50), font)
# button.draw(screen)
# if button.is_clicked(mouse_pos):
#     print('Button clicked')

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
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
        
        self.obj_model = OBJLoader('path/to/your/model.obj')
        
        self.texture_id = self.load_texture("texture.png")
        self.init_lighting()

        self.font = pygame.font.SysFont('Arial', 18)
        self.buttons = [
            Button('Start', (10, 10), (100, 50), self.font),
            Button('Stop', (10, 70), (100, 50), self.font)
        ]
        self.running = True

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

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
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
        
        self.render_text(f'Cube Position: {self.cube1.position}', (10, 130))
        
        for button in self.buttons:
            button.draw(self.screen)
        
        pygame.display.flip()
        pygame.time.wait(10)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            self.handle_button_click(button)

            self.handle_input()
            self.update()
        pygame.quit()
    
    def handle_button_click(self, button):
        if button.text == 'Start':
            self.running = True
        elif button.text == 'Stop':
            self.running = False

if __name__ == "__main__":
    engine = GameEngine(800, 600)
    engine.run()
##############################################################
class GameObjectManager:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update(self, delta_time):
        for obj in self.objects:
            obj.update(delta_time)

    def draw(self):
        for obj in self.objects:
            obj.draw()

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        self.rotation = [0, 0, 0]
        self.mouse_sensitivity = 0.1
        self.last_mouse_pos = pygame.mouse.get_pos()

        self.physics_engine = PhysicsEngine()
        self.obj_model = OBJLoader('path/to/your/model.obj')
        
        self.texture_id = self.load_texture("texture.png")
        self.init_lighting()

        self.font = pygame.font.SysFont('Arial', 18)
        self.buttons = [
            Button('Start', (10, 10), (100, 50), self.font),
            Button('Stop', (10, 70), (100, 50), self.font)
        ]
        self.running = True

        self.game_object_manager = GameObjectManager()
        self.cube1 = GameObject([0, 0, 0], [1, 1, 1], [0, 0, 0])
        self.cube2 = GameObject([2, 0, 0], [1, 1, 1], [0, 0, 0], dynamic=False)
        self.game_object_manager.add_object(self.cube1)
        self.game_object_manager.add_object(self.cube2)

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

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
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
        self.game_object_manager.draw()
        self.draw_obj_model()
        glPopMatrix()
        
        self.render_text(f'Cube Position: {self.cube1.position}', (10, 130))
        
        for button in self.buttons:
            button.draw(self.screen)
        
        pygame.display.flip()
        pygame.time.wait(10)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            self.handle_button_click(button)

            self.handle_input()
            self.update()
        pygame.quit()
    
    def handle_button_click(self, button):
        if button.text == 'Start':
            self.running = True
        elif button.text == 'Stop':
            self.running = False

if __name__ == "__main__":
    engine = GameEngine(800, 600)
    engine.run()
##############################################################
class RigidBody:
    def __init__(self, mass=1.0, inertia=np.array([1, 1, 1]), velocity=np.array([0, 0, 0]), angular_velocity=np.array([0, 0, 0])):
        self.mass = mass
        self.inertia = inertia
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.forces = np.array([0, 0, 0])
        self.torques = np.array([0, 0, 0])

    def apply_force(self, force, point=np.array([0, 0, 0])):
        self.forces += force
        self.torques += np.cross(point, force)

    def update(self, delta_time):
        acceleration = self.forces / self.mass
        self.velocity += acceleration * delta_time
        self.forces = np.array([0, 0, 0])

        angular_acceleration = self.torques / self.inertia
        self.angular_velocity += angular_acceleration * delta_time
        self.torques = np.array([0, 0, 0])

