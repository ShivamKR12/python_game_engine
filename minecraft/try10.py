from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import OpenSimplex

app = Ursina()

# Initialize OpenSimplex noise generator
noise_gen = OpenSimplex(seed=42)

a = Audio('assets/song_Forest.mp3', pitch=1, loop=True, autoplay=True)
a.volume=5
window.title = 'Minecraft_clone'        # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = False     # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True
window.cursor_hidden = False

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

# Global variable to store voxels
voxels = {}

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
    update_voxels()

def update_voxels():
    for voxel in voxels.values():
        voxel.update()

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
        self.enabled = False  # Initially disable rendering
        self.position = position  # Initialize position
        self.update()  # Call update initially to set initial visibility

    def update(self):
        distance_to_player = distance(self.position, player.position)
        if distance_to_player > 3:  # Adjust the visibility distance as needed
            self.disable()
        else:
            self.enable()

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position=self.position + mouse.normal, texture=current_texture)
            elif key == "right mouse down":
                destroy(self)

    def disable(self):
        if self.enabled:
            self.enabled = False

    def enable(self):
        if not self.enabled:
            self.enabled = True

player = FirstPersonController()

chunk_size = 16  # Number of voxels in each dimension of a chunk
subchunk_size = 8  # Number of voxels in each dimension of a subchunk

def generate_chunk(cx, cz):
    global voxels
    for y in range(-3, 4):  # Adjust the range to include blocks both above and below the player
        for z in range(cz * chunk_size, (cz + 1) * chunk_size):
            for x in range(cx * chunk_size, (cx + 1) * chunk_size):
                noise_val = noise_gen.noise3(x * 0.1, y * 0.1, z * 0.1)  # Adjust the scale as needed
                if y == 0:  # Spawn grass blocks
                    voxels[(x, y, z)] = Voxel((x, y, z), texture=textures['grass'])
                elif y < noise_val * 10:  # Spawn dirt blocks below grass based on noise
                    voxels[(x, y, z)] = Voxel((x, y, z), texture=textures['soil'])

def generate_world():
    global voxels
    for cz in range(-3, 4):  # Adjust the range to include chunks both above and below the player
        for cx in range(-3, 4):
            generate_chunk(cx, cz)

generate_world()

sky = Entity(model='sphere', scale=500, texture=textures['sky'], double_sided=True)

app.run()
