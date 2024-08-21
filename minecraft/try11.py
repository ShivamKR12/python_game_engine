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

voxels = {}

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

def update_voxels():
    for voxel in voxels.values():
        voxel.update()

player = FirstPersonController()

import math

chunk_size = 8  # Adjust the chunk size as needed
render_distance = 5  # Adjust the render distance as needed

# Function to group blocks into chunks
def get_chunk_key(x, y, z):
    return x // chunk_size, y // chunk_size, z // chunk_size

chunks = {}

# Function to check if a chunk is within the player's field of view
def is_chunk_visible(chunk_key):
    player_position = Vec3(player.x, player.y, player.z)
    chunk_position = Vec3(chunk_key[0] * chunk_size, chunk_key[1] * chunk_size, chunk_key[2] * chunk_size)
    direction_to_chunk = (chunk_position - player_position).normalize()
    # angle = math.degrees(math.acos(direction_to_chunk.dot(player.forward)))
    # return angle < 90  # Adjust the field of view angle as needed

# Update chunks based on player position and visibility
def update_chunks():
    player_chunk_key = get_chunk_key(int(player.x), int(player.y), int(player.z))

    for chunk_key, chunk_blocks in list(chunks.items()):
        if not is_chunk_visible(chunk_key):
            for block_pos in chunk_blocks:
                voxels.pop(block_pos)
            chunks.pop(chunk_key)

    for y in range(player_chunk_key[1] - render_distance, player_chunk_key[1] + render_distance + 1):
        for z in range(player_chunk_key[2] - render_distance, player_chunk_key[2] + render_distance + 1):
            for x in range(player_chunk_key[0] - render_distance, player_chunk_key[0] + render_distance + 1):
                chunk_key = (x, y, z)
                if chunk_key not in chunks:
                    if is_chunk_visible(chunk_key):
                        chunk_blocks = []
                        for dy in range(chunk_size):
                            for dz in range(chunk_size):
                                for dx in range(chunk_size):
                                    block_pos = (x * chunk_size + dx, y * chunk_size + dy, z * chunk_size + dz)
                                    noise_val = noise_gen.noise3(block_pos[0] * 0.1, block_pos[1] * 0.1, block_pos[2] * 0.1)
                                    if block_pos[1] == 0:  # Spawn grass blocks
                                        voxels[block_pos] = Voxel(block_pos, texture=textures['grass'])
                                    elif block_pos[1] < noise_val * 10:  # Spawn dirt blocks below grass based on noise
                                        voxels[block_pos] = Voxel(block_pos, texture=textures['soil'])
                                    elif block_pos[1] > noise_val * 10:  # Spawn ceiling blocks above noise
                                        if (block_pos[0], block_pos[1]-1, block_pos[2]) in voxels and voxels[(block_pos[0], block_pos[1]-1, block_pos[2])].texture == textures['wall_2']:
                                            continue  # Skip if block below is already part of ceiling
                                        else:
                                            chunk_blocks.append(block_pos)
                        chunks[chunk_key] = chunk_blocks

# Initial chunk generation based on player starting position
update_chunks()

# Update chunks continuously while the game is running
def update():
    player.update()
    update_chunks()
    update_voxels()

sky = Entity(model='sphere', scale=150, texture=textures['sky'], double_sided=True)

app.run()
