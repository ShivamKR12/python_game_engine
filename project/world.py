# world.py

from panda3d.core import NodePath, Loader

class World:
    def __init__(self, render, loader: Loader):
        self.render = render
        self.loader = loader
        self.load_map()
        self.load_objects()

    def load_map(self):
        self.map = self.loader.loadModel("models/map")
        self.map.reparentTo(self.render)

    def load_objects(self):
        # Load additional objects into the world here
        pass

    def draw(self):
        self.map.draw()
