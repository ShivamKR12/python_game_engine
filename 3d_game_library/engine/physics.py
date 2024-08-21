import numpy as np

class PhysicsObject:
    def __init__(self, mass=1.0, position=(0, 0, 0), velocity=(0, 0, 0)):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def apply_force(self, force, delta_time):
        acceleration = np.array(force) / self.mass
        self.velocity += acceleration * delta_time

    def update(self, delta_time):
        self.position += self.velocity * delta_time

class SimplePhysicsEngine:
    def __init__(self, gravity=(0, 0, -9.81)):
        self.gravity = np.array(gravity, dtype=float)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, delta_time):
        for obj in self.objects:
            obj.apply_force(self.gravity * obj.mass, delta_time)
            obj.update(delta_time)
