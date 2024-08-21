
from glm import vec3
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE
from player import Player
from world import World
from enemy import Enemy
from collision import collision_manager
from direct.task import Task

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.initialize_panda3d()
        self.create_window()
        self.player = Player(self.render)
        self.world = World(self.render, self.loader)
        self.enemy = Enemy(self.render, vec3(10, 0, 0), self.player)
        self.taskMgr.add(self.game_loop, "gameLoop")

    def initialize_panda3d(self):
        loadPrcFileData("", f"win-size {SCREEN_WIDTH} {SCREEN_HEIGHT}")
        loadPrcFileData("", f"show-frame-rate-meter #t")
        self.setFrameRateMeter(True)

    def create_window(self):
        self.setBackgroundColor(0, 0, 0)
        self.disableMouse()

    def game_loop(self, task):
        dt = globalClock.getDt()
        self.player.update(dt)
        collision_manager.check_collisions()
        return Task.cont

app = MyApp()
app.run()
