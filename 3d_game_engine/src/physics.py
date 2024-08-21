import numpy as np
from pyrr import Vector3
from utils import load_model, load_model_from_file

GRAVITY = Vector3([0, -9.81, 0])

class PhysicsEngine:
    def __init__(self, gravity=GRAVITY, friction=0.9, restitution=0.8):
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

    def update(self, delta_time):
        self.position += self.velocity * delta_time

class RigidBody(GameObject):
    def __init__(self, position, mass=1.0, size=Vector3([1.0, 1.0, 1.0]), dynamic=True):
        super().__init__(position, size, [0, 0, 0], dynamic)
        self.mass = mass
        self.vao = None
        self.vertex_count = 0

    def load_model(self, model_path):
        vao_list, vertex_counts, _ = load_model_from_file(model_path)
        if vao_list:
            self.vao = vao_list[0]
            self.vertex_count = vertex_counts[0]

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self, delta_time):
        super().update(delta_time)
