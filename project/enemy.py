# enemy.py

from panda3d.core import NodePath, Vec3, CollisionNode, CollisionSphere
from direct.actor.Actor import Actor
from direct.task import Task
from collision import collision_manager

class Enemy:
    def __init__(self, render, position, player):
        self.actor = Actor("models/enemy", {"walk": "models/enemy-walk"})
        self.actor.reparentTo(render)
        self.actor.setScale(0.2, 0.2, 0.2)
        self.actor.setPos(position)
        self.move_speed = 2
        self.health = 100
        self.player = player

        # Set up collision detection
        self.collider = self.actor.attachNewNode(CollisionNode('enemy_cnode'))
        self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        collision_manager.add_collider(self.collider, self)

        self.taskMgr = render.taskMgr
        self.taskMgr.add(self.update, "enemyTask")

    def update(self, task):
        dt = globalClock.getDt()
        self.move(dt)
        return Task.cont

    def move(self, dt):
        direction = self.player.actor.getPos() - self.actor.getPos()
        direction.normalize()
        move_vector = direction * self.move_speed * dt
        self.actor.setPos(self.actor.getPos() + move_vector)

    def draw(self):
        self.actor.draw()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.actor.removeNode()
        self.alive = False

    def handle_collision(self, other):
        pass  # Implement additional collision handling logic here
