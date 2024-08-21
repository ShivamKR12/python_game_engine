from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Load textures
textures = {
    'grass': load_texture("assets/download.jpg"),
    'soil': load_texture("assets/soil.jpg"),
    'tree': load_texture("assets/tree.jpg"),
    'plank': load_texture("assets/planks.jpg"),
    'leaf': load_texture("assets/leaf.jpg"),
    'wall': load_texture("assets/wall.jpg"),
    'stone': load_texture("assets/stone.png"),
    'iron': load_texture("assets/images.png"),
    'gold': load_texture("assets/gold.png"),
    'wall_2': load_texture("assets/1.png"),
    'sky': load_texture("assets/sky.jpg")
}

# Current texture
current_texture = textures['soil']

def update():
    global current_texture
    if held_keys['q'] or held_keys['Q']:
        exit()

    if held_keys['1']: current_texture = textures['grass']
    if held_keys['2']: current_texture = textures['soil']
    if held_keys['3']: current_texture = textures['tree']
    if held_keys['4']: current_texture = textures['plank']
    if held_keys['5']: current_texture = textures['leaf']
    if held_keys['6']: current_texture = textures['wall']
    if held_keys['7']: current_texture = textures['stone']
    if held_keys['8']: current_texture = textures['gold']
    if held_keys['9']: current_texture = textures['iron']
    if held_keys['0']: current_texture = textures['wall_2']

    player.update()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=textures['grass']):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.white,
            texture=texture,
            highlight_color=color.white,
            position=position,
            origin_y=0.5
        )

    def update(self):
        distance_to_player = distance(self.position, player.position)
        if distance_to_player > 10:  # Adjust the visibility distance as needed
            self.enabled = False
        else:
            self.enabled = True

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position=self.position + mouse.normal, texture=current_texture)
            elif key == "right mouse down":
                destroy(self)

for y in range(-3, 4):  # Adjust the range to include blocks both above and below the player
    for z in range(-3, 3):
        for x in range(-3, 3):
            if y == 0:  # Spawn grass blocks
                voxel = Voxel((x, y, z), texture=textures['grass'])
            elif y < 0:  # Spawn dirt blocks below grass
                voxel = Voxel((x, y, z), texture=textures['soil'])

player = FirstPersonController()
sky = Entity(model='sphere', scale=150, texture=textures['sky'], double_sided=True)

app.run()
