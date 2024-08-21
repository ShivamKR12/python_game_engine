from ursina import *  # Import all symbols from the Ursina module

from ursina.prefabs.first_person_controller import FirstPersonController  # Import the FirstPersonController prefab

app = Ursina()  # Initialize the Ursina application

# Load and play background music
a = Audio('assets/song_Forest.mp3', pitch=1, loop=True, autoplay=True)
a.volume=5  # Set the volume of the audio

window.title = 'Minecraft_clone'  # Set the window title
window.borderless = False  # Show a border for the window
window.fullscreen = False  # Do not make the window fullscreen
window.exit_button.visible = False  # Hide the exit button
window.fps_counter.enabled = True  # Enable the FPS counter
window.cursor_hidden = False  # Show the cursor

# Load textures for various blocks and objects
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

# Set the initial texture
current_texture = textures['soil']

def update():
    global current_texture
    if held_keys['q'] or held_keys['Q']:  # If Q or q is pressed, exit the application
        exit()

    # Change the current texture based on the pressed number keys
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

    player.update()  # Update the first person controller
    update_voxels()  # Update the voxels in the scene

voxels = {}  # Dictionary to store voxels

# Define a class for each voxel block
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=textures['grass']):
        super().__init__(
            parent=scene,  # Set the parent entity to be the scene
            model='cube',  # Set the model to be a cube
            color=color.white,  # Set the color of the voxel
            texture=texture,  # Set the texture of the voxel
            highlight_color=color.white,  # Set the highlight color of the voxel
            position=position,  # Set the initial position of the voxel
            origin_y=0.5  # Set the origin point of the voxel to be at its center
        )
        self.enabled = False  # Initially disable rendering
        self.update()  # Call update initially to set initial visibility

    # Update the visibility of the voxel based on the distance to the player
    def update(self):
        distance_to_player = distance(self.position, player.position)
        if distance_to_player > 3:  # Adjust the visibility distance as needed
            self.disable()  # Disable rendering if the distance is beyond the visibility range
        else:
            self.enable()  # Enable rendering if within the visibility range

    # Handle user input for placing and destroying voxels
    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position=self.position + mouse.normal, texture=current_texture)
            elif key == "right mouse down":
                destroy(self)

    # Disable rendering of the voxel
    def disable(self):
        if self.enabled:
            self.enabled = False

    # Enable rendering of the voxel
    def enable(self):
        if not self.enabled:
            self.enabled = True

# Update the visibility of all voxels in the scene
def update_voxels():
    for voxel in voxels.values():
        voxel.update()

player = FirstPersonController()  # Initialize the first person controller

# Generate voxels for the scene
for y in range(-3, 4):  # Adjust the range to include blocks both above and below the player
    for z in range(-10, 10):
        for x in range(-10, 10):
            if y == 0:  # Spawn grass blocks at y=0
                voxels[(x, y, z)] = Voxel((x, y, z), texture=textures['grass'])
            elif y < 0:  # Spawn dirt blocks below grass
                voxels[(x, y, z)] = Voxel((x, y, z), texture=textures['soil'])

# Create a sky entity
sky = Entity(model='sphere', scale=150, texture=textures['sky'], double_sided=True)

app.run()  # Run the Ursina application
