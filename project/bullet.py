# bullet.py

from panda3d.core import Vec3, NodePath, CollisionNode, CollisionSphere
from direct.task import Task
from collision import collision_manager
from project.enemy import Enemy

class Bullet:
    def __init__(self, render, start_pos, direction):
        self.render = render
        self.node = NodePath("bullet")
        self.node.reparentTo(render)
        self.node.setPos(start_pos)
        self.direction = direction
        self.speed = 50
        self.alive = True

        # Set up collision detection
        self.collider = self.node.attachNewNode(CollisionNode('bullet_cnode'))
        self.collider.node().addSolid(CollisionSphere(0, 0, 0, 0.2))
        collision_manager.add_collider(self.collider, self)

        self.taskMgr = render.taskMgr
        self.taskMgr.add(self.update, "bulletTask")

    def update(self, task):
        if not self.alive:
            return Task.done
        dt = globalClock.getDt()
        move_vector = self.direction * self.speed * dt
        self.node.setPos(self.node.getPos() + move_vector)
        return Task.cont

    def handle_collision(self, other):
        if isinstance(other, Enemy):
            other.take_damage(10)
            self.alive = False
            self.node.removeNode()

    def draw(self):
        pass  # Draw bullet here
