from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Textures
grass_texture = load_texture("assets/download.jpg")
soil_texture = load_texture("assets/soil.jpg")
tree_texture = load_texture("assets/tree.jpg")
plank_texture = load_texture("assets/planks.jpg")
leaf_texture = load_texture("assets/leaf.jpg")
wall_texture = load_texture("assets/wall.jpg")
stone_texture = load_texture("assets/stone.png")
iron_texture = load_texture("assets/images.png")
gold_texture = load_texture("assets/gold.png")
wall_2_texture = load_texture("assets/1.png")
sky_texture = load_texture("assets/sky.jpg")

# Current texture
current_texture = soil_texture

class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='quad',
            scale=(0.1, 0.2),  # Adjust the scale as needed
            origin=(0, 0),  # Set origin to bottom-left corner
            position=(-0.5, 0.4),  # Adjust position as needed
            texture='white_cube',
            color=color.color(0, 0, 0, a=0.5),  # Set a semi-transparent black color
            enabled=False
        )

        # List to store inventory items
        self.items = []

    def add_item(self, item_texture):
        # Create a new item entity and add it to the inventory
        new_item = Entity(
            parent=self,
            model='quad',
            texture=item_texture,
            scale=(0.1, 0.1),  # Adjust scale as needed
            position=(len(self.items) * 0.1, 0),  # Adjust position to align items horizontally
        )
        self.items.append(new_item)

    def clear_inventory(self):
        # Destroy all items in the inventory
        for item in self.items:
            destroy(item)
        self.items = []

inventory = Inventory()
inventory_open = False  # Flag to track if inventory is open

def update():
    global current_texture, inventory_open

    if held_keys['q'] or held_keys['Q']:
        exit()

    if held_keys['1']: current_texture = grass_texture
    elif held_keys['2']: current_texture = soil_texture
    elif held_keys['3']: current_texture = tree_texture
    elif held_keys['4']: current_texture = plank_texture
    elif held_keys['5']: current_texture = leaf_texture
    elif held_keys['6']: current_texture = wall_texture
    elif held_keys['7']: current_texture = stone_texture
    elif held_keys['8']: current_texture = gold_texture
    elif held_keys['9']: current_texture = iron_texture
    elif held_keys['0']: current_texture = wall_2_texture

    if held_keys['i'] or held_keys['I']:
        if not inventory_open:  # Toggle inventory visibility only once per press
            inventory.enabled = not inventory.enabled
            inventory_open = True
    else:
        inventory_open = False  # Reset flag when 'i' key is released

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
            origin_y=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position=self.position + mouse.normal, texture=current_texture)
            elif key == "right mouse down":
                destroy(self)

for z in range(6):
    for x in range(6):
        voxel = Voxel((x, 0, z), texture=grass_texture)

t = -1
while t >= -10:
    for z in range(6):
        for x in range(6):
            voxel = Voxel((x, t, z), texture=soil_texture)
    t -= 1

player = FirstPersonController()
sky = Sky()
app.run()
