# collision.py

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionSphere

class CollisionManager:
    def __init__(self):
        self.traverser = CollisionTraverser()
        self.handler = CollisionHandlerQueue()

    def add_collider(self, collider, obj):
        self.traverser.add_collider(collider, self.handler)
        collider.node().setPythonTag("owner", obj)

    def check_collisions(self):
        self.traverser.traverse(render)
        for entry in self.handler.entries:
            collider = entry.getFromNodePath()
            collidee = entry.getIntoNodePath()
            collider_obj = collider.node().getPythonTag("owner")
            collidee_obj = collidee.node().getPythonTag("owner")
            if collider_obj and collidee_obj:
                collider_obj.handle_collision(collidee_obj)

collision_manager = CollisionManager()
