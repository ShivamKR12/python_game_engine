from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
#from  ursina.prefabs.exit_button import *

t = -1
app = Ursina()
a = Audio('assets/song_Forest.mp3', pitch=1, loop=True, autoplay=True)
a.volume=5
window.title = 'Minecraft_clone'        # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
#window.exit_button.visible = False     # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True
window.cursor_hidden = False
#window.icon = "/assets/tree.jpg"

grass_texture = load_texture("assets/download.jpg")
sky_texture = load_texture("assets/sky.jpg")
soil_texture = load_texture("assets/soil.jpg")
tree_texture = load_texture("assets/tree.jpg")
plank_texture = load_texture("assets/planks.jpg")
leaf_texture = load_texture("assets/leaf.jpg")
wall_texture = load_texture("assets/wall.jpg")
stone_texture  = load_texture("assets/stone.png")
iron_texture = load_texture("assets/images.png")
gold_texture = load_texture("assets/gold.png")
wall_2_texture = load_texture("assets/1.png")
current_texture = soil_texture


def update():
    global current_texture
    if held_keys['q']: exit()
    if held_keys['Q']: exit()
    if held_keys['1']: current_texture = grass_texture
    if held_keys['2']: current_texture = soil_texture
    if held_keys['3']: current_texture = tree_texture
    if held_keys['4']: current_texture = plank_texture
    if held_keys['5']: current_texture = leaf_texture
    if held_keys['6']: current_texture = wall_texture
    if held_keys['7']: current_texture = stone_texture
    if held_keys['8']: current_texture = gold_texture
    if held_keys['9']: current_texture = iron_texture
    if held_keys['0']: current_texture = wall_2_texture

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            scale=150,
            texture=sky_texture,
            double_sided=True
        )


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.white,
            texture=texture,
            highlight_color=color.white,
            position=position,
            origin__y=0.5
        )

    def input(self, key):

        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position=self.position + mouse.normal, texture= current_texture)
            if key == "right mouse down":
                destroy(self)


for z in range(6):
    for x in range(6):
        voxel = Voxel((x, 0, z), texture= grass_texture)
while t >= -10:
    for z in range(6):
        for x in range(6):
            voxel = Voxel((x, t, z) , texture= soil_texture)
    t-=1

player = FirstPersonController()
sky = Sky()
app.run()
