# player.py

from panda3d.core import Vec3
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from bullet import Bullet

class Player(DirectObject):
    def __init__(self, render):
        self.actor = Actor("models/player", {"walk": "models/player-walk"})
        self.actor.reparentTo(render)
        self.actor.setScale(0.2, 0.2, 0.2)
        self.actor.setPos(0, 0, 0)
        self.setup_controls()
        self.move_speed = 5
        self.jump_speed = 10
        self.is_jumping = False
        self.bullets = []

    def setup_controls(self):
        self.key_map = {"left": 0, "right": 0, "forward": 0, "backward": 0, "jump": 0, "shoot": 0}
        self.accept("arrow_left", self.update_key_map, ["left", 1])
        self.accept("arrow_left-up", self.update_key_map, ["left", 0])
        self.accept("arrow_right", self.update_key_map, ["right", 1])
        self.accept("arrow_right-up", self.update_key_map, ["right", 0])
        self.accept("arrow_up", self.update_key_map, ["forward", 1])
        self.accept("arrow_up-up", self.update_key_map, ["forward", 0])
        self.accept("arrow_down", self.update_key_map, ["backward", 1])
        self.accept("arrow_down-up", self.update_key_map, ["backward", 0])
        self.accept("space", self.update_key_map, ["jump", 1])
        self.accept("space-up", self.update_key_map, ["jump", 0])
        self.accept("mouse1", self.update_key_map, ["shoot", 1])
        self.accept("mouse1-up", self.update_key_map, ["shoot", 0])

    def update_key_map(self, key, value):
        self.key_map[key] = value

    def update(self, dt):
        self.move(dt)
        self.jump(dt)
        if self.key_map["shoot"]:
            self.shoot()

        # Update bullets
        for bullet in self.bullets:
            bullet.update(dt)

    def move(self, dt):
        move_vector = Vec3(
            self.key_map["right"] - self.key_map["left"],
            self.key_map["forward"] - self.key_map["backward"],
            0,
        )
        move_vector.normalize()
        move_vector *= self.move_speed * dt
        self.actor.setPos(self.actor.getPos() + move_vector)

    def jump(self, dt):
        if self.key_map["jump"] and not self.is_jumping:
            self.is_jumping = True
            self.actor.setZ(self.actor.getZ() + self.jump_speed * dt)
        if self.actor.getZ() <= 0:
            self.is_jumping = False
            self.actor.setZ(0)

    def shoot(self):
        direction = Vec3(1, 0, 0)  # Change this based on where the player is facing
        start_pos = self.actor.getPos()
        bullet = Bullet(self.actor, start_pos, direction)
        self.bullets.append(bullet)
