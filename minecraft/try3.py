from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

t = -1
app = Ursina()

a = Audio('assets/song_Forest.mp3', pitch=1, loop=True, autoplay=True)
a.volume=5

window.title = 'Minecraft_clone'        # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.fps_counter.enabled = True
window.cursor_hidden = False

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


class Inventory(Entity):
    def __init__(self, width=5, height=8, **kwargs):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (width, height),
            scale = (width*.1, height*.1),
            origin = (-.5,.5),
            position = (-.3,.4),
            color = color.color(0, 0, .1, .9),
            enabled = False  # initially set inventory to disabled
            )

        self.width = width
        self.height = height

        for key, value in kwargs.items():
            setattr(self, key, value)


    def find_free_spot(self):
        for y in range(self.height):
            for x in range(self.width):
                grid_positions = [(int(e.x*self.texture_scale[0]), int(e.y*self.texture_scale[1])) for e in self.children]
                print(grid_positions)

                if not (x, -y) in grid_positions:
                    print('found free spot:', x, y)
                    return x, y


    def append(self, item, x=0, y=0):
        print('add item:', item)

        if len(self.children) >= self.width*self.height:
            print('inventory full')
            error_message = Text('<red>Inventory is full!', origin=(0,-1.5), x=-.5, scale=2)
            destroy(error_message, delay=1)
            return

        x, y = self.find_free_spot()

        icon = Draggable(
            parent = self,
            model = 'quad',
            texture = item,
            color = color.white,
            scale_x = 1/self.texture_scale[0],
            scale_y = 1/self.texture_scale[1],
            origin = (-.5,.5),
            x = x * 1/self.texture_scale[0],
            y = -y * 1/self.texture_scale[1],
            z = -.5,
            )
        name = item.replace('_', ' ').title()

        if random.random() < .25:
            icon.color = color.gold
            name = '<orange>Rare ' + name

        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.color(0,0,0,.8)


        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z -= .01   # ensure the dragged item overlaps the rest

        def drop():
            icon.x = int((icon.x + (icon.scale_x/2)) * self.width) / self.width
            icon.y = int((icon.y - (icon.scale_y/2)) * self.height) / self.height
            icon.z += .01

            # if outside, return to original position
            if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                icon.position = (icon.org_pos)
                return

            # if the spot is taken, swap positions
            for c in self.children:
                if c == icon:
                    continue

                if c.x == icon.x and c.y == icon.y:
                    print('swap positions')
                    c.position = icon.org_pos

        icon.drag = drag
        icon.drop = drop

        # Add close functionality to inventory
        def input(key):
            if key == 'escape':
                self.enabled = False

        self.input = input


inventory = Inventory()

def add_item():
    inventory.append(random.choice(('bag', 'bow_arrow', 'gem', 'orb', 'sword')))

add_item()
add_item()
add_item_button = Button(
    scale = (.1,.1),
    x = -.5,
    color = color.lime.tint(-.25),
    text = '+',
    tooltip = Tooltip('Add random item'),
    on_click = add_item
    )
background = Entity(parent=camera.ui, model='quad', texture='shore', scale_x=camera.aspect_ratio, z=1)

Cursor(texture='cursor', scale=.1)
mouse.visible = False

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
