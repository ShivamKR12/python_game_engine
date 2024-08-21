from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.exit_button import ExitButton
from numpy import random, sin, cos
from opensimplex import OpenSimplex
import json
import random
import numpy


t = -1
app = Ursina()
a = Audio('assets/song_Forest.mp3', pitch=1, loop=True, autoplay=True)
a.volume = 5
window.title = 'Minecraft_clone'  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.exit_button = ExitButton(visible=False)  # Do not show the in-game red X that closes the window
window.fps_counter.enabled = True
window.cursor_visible = True

grass_texture = load_texture("assets/download.jpg")
sky_texture = load_texture("assets/sky.jpg")
soil_texture = load_texture("assets/soil.jpg")
tree_texture = load_texture("assets/tree.jpg")
plank_texture = load_texture("assets/planks.jpg")
leaf_texture = load_texture("assets/leaf.jpg")
wall_texture = load_texture("assets/wall.jpg")
stone_texture = load_texture("assets/stone.png")
iron_texture = load_texture("assets/images.png")
gold_texture = load_texture("assets/gold.png")
wall_2_texture = load_texture("assets/1.png")
current_texture = soil_texture


def update():
    global current_texture
    if held_keys['q'] or held_keys['Q']:
        exit()
    if held_keys['1']:
        current_texture = grass_texture
    elif held_keys['2']:
        current_texture = soil_texture
    elif held_keys['3']:
        current_texture = tree_texture
    elif held_keys['4']:
        current_texture = plank_texture
    elif held_keys['5']:
        current_texture = leaf_texture
    elif held_keys['6']:
        current_texture = wall_texture
    elif held_keys['7']:
        current_texture = stone_texture
    elif held_keys['8']:
        current_texture = gold_texture
    elif held_keys['9']:
        current_texture = iron_texture
    elif held_keys['0']:
        current_texture = wall_2_texture


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
            if key == "right mouse down":
                destroy(self)


class Light(Entity):
    def __init__(self, position):
        super().__init__(
            parent=scene,
            model='sphere',
            scale=0.5,
            color=color.white,
            position=position
        )


light = Light((0, 5, 0))

class Terrain:
    def __init__(self, width, depth, height_multiplier):
        self.vertices = []
        self.normals = []

        opensimplex = OpenSimplex(seed=42)

        for i in range(width + 1):
            for j in range(depth + 1):
                x = i / width
                z = j / depth
                y = opensimplex.noise2(x * height_multiplier, z * height_multiplier)
                self.vertices.extend([x, y, z])
                self.normals.extend([0, 1, 0])  # Assuming normal vector is always (0, 1, 0)

        # Convert vertices and normals to numpy arrays
        self.vertices = numpy.array(self.vertices, dtype=numpy.float32)
        self.normals = numpy.array(self.normals, dtype=numpy.float32)

        # The Mesh class expects boolean values for colors, UVs, and normals
        colors = numpy.zeros(len(self.vertices), dtype=bool)
        uvs = numpy.zeros(len(self.vertices), dtype=bool)
        normals = numpy.ones(len(self.vertices), dtype=bool)  # Set normals to True for all vertices

        self.model = Mesh(vertices=self.vertices, colors=colors, uvs=uvs, normals=normals, mode='triangles')


terrain = Terrain(100, 100, 20)


class Resource:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Player:
    def __init__(self):
        self.resources = {}

    def collect_resource(self, resource):
        if resource.name not in self.resources:
            self.resources[resource.name] = 0
        self.resources[resource.name] += resource.amount

    def use_resource(self, resource_name, amount):
        if resource_name not in self.resources:
            print(f"You don't have any {resource_name}.")
            return
        if self.resources[resource_name] < amount:
            print(f"You don't have enough {resource_name}.")
            return
        self.resources[resource_name] -= amount


player = Player()
stone = Resource("stone", 10)
player.collect_resource(stone)
player.use_resource("stone", 5)


class Item:
    def __init__(self, name, texture):
        self.name = name
        self.texture = texture


class CraftingRecipe:
    def __init__(self, input_items, output_item):
        self.input_items = input_items
        self.output_item = output_item


class CraftingTable(Entity):
    def __init__(self, position):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.brown,
            texture=load_texture("assets/crafting_table.png"),
            position=position,
            origin_y=0.5
        )
        self.crafting_interface = CraftingInterface()


class CraftingInterface:
    def __init__(self):
        self.input_items = {}
        self.output_items = {}

    def add_input_item(self, item):
        if item.name not in self.input_items:
            self.input_items[item.name] = 0
        self.input_items[item.name] += 1

    def remove_input_item(self, item):
        if item.name not in self.input_items:
            return
        self.input_items[item.name] -= 1

    def add_output_item(self, item):
        if item.name not in self.output_items:
            self.output_items[item.name] = 0
        self.output_items[item.name] += 1

    def remove_output_item(self, item):
        if item.name not in self.output_items:
            return
        self.output_items[item.name] -= 1

    def craft(self, recipe):
        for input_item in recipe.input_items:
            if input_item.name not in self.input_items or self.input_items[input_item.name] < recipe.input_items[
                input_item.name]:
                return
            for input_item in recipe.input_items:
                self.remove_input_item(input_item)
            for output_item in recipe.output_items:
                self.add_output_item(output_item)


crafting_table = CraftingTable((0, 0, 0))

stone_pickaxe_recipe = CraftingRecipe({"stick": 2, "stone": 3}, {"stone_pickaxe": 1})

crafting_interface = crafting_table.crafting_interface

stick = Item("stick", load_texture("assets/stick.png"))
stone = Item("stone", load_texture("assets/stone.png"))
stone_pickaxe = Item("stone_pickaxe", load_texture("assets/stone_pickaxe.png"))

crafting_interface.add_input_item(stick)
crafting_interface.add_input_item(stick)
crafting_interface.add_input_item(stone)
crafting_interface.add_input_item(stone)
crafting_interface.add_input_item(stone)

crafting_interface.craft(stone_pickaxe_recipe)

assert crafting_interface.output_items["stone_pickaxe"] == 1




class GameState:
    def __init__(self):
        self.player = {
            "position": (0, 0, 0),
            "resources": {}
        }
        self.voxels = []

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.__dict__, f)

    def load(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            self.__dict__.update(data)


game_state = GameState()
game_state.save("save.json")
game_state.load("save.json")


class Player:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.max_experience = 100
        self.skills = {}

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.max_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_experience *= 1.5
        self.add_skill_point()

    def add_skill_point(self):
        self.skills["strength"] = self.skills.get("strength", 0) + 1


player = Player()
player.add_experience(100)
player.add_experience(100)

assert player.level == 3
assert player.skills["strength"] == 2


class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards

    def is_complete(self):
        for objective in self.objectives:
            if not objective.is_complete:
                return False
        return True

    def complete(self):
        for objective in self.objectives:
            objective.complete()
        for reward in self.rewards:
            reward.receive()


class Objective:
    def __init__(self, name, description, is_complete):
        self.name = name
        self.description = description
        self.is_complete = is_complete

    def complete(self):
        self.is_complete = True


class Reward:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def receive(self):
        # Give the player the reward
        pass


quest = Quest(
    "Kill the goblin",
    "Kill the goblin that is terrorizing the village.",
    [
        Objective("Kill the goblin", "Kill the goblin that is terrorizing the village.", False)
    ],
    [
        Reward("experience", 50),
        Reward("gold", 100)
    ]
)

player = Player()

# The player completes the quest objective
quest.objectives[0].complete()

assert quest.is_complete()
quest.complete()

assert player.experience == 50
assert player.resources["gold"] == 100


class Block:
    def __init__(self, name, texture):
        self.name = name
        self.texture = texture


class Player:
    def __init__(self):
        self.inventory = {
            "blocks": []
        }

    def add_block(self, block):
        self.inventory["blocks"].append(block)

    def remove_block(self, block):
        self.inventory["blocks"].remove(block)


class BuildingPlan:
    def __init__(self, name, blocks):
        pass





class Weather:
    def __init__(self):
        self.weather_type = "clear"
        self.chance_of_rain = 0.1
        self.chance_of_snow = 0.01
        self.chance_of_wind = 0.05

    def update(self):
        if random.random() < self.chance_of_rain:
            self.weather_type = "rain"
        elif random.random() < self.chance_of_snow:
            self.weather_type = "snow"
        elif random.random() < self.chance_of_wind:
            self.weather_type = "wind"
        else:
            self.weather_type = "clear"


weather = Weather()


class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue

    def talk(self):
        print(self.dialogue)


npc = NPC("villager", "Hello, how can I help you?")
npc.talk()


def generate_terrain(width, depth, height_multiplier):
    opensimplex = OpenSimplex()
    terrain = []
    for i in range(width):
        row = []
        for j in range(depth):
            x = i / width
            z = j / depth
            y = opensimplex.noise2d(x * height_multiplier, z * height_multiplier)
            row.append(y)
        terrain.append(row)
    return terrain


terrain = generate_terrain(100, 100, 20)

for z in range(6):
    for x in range(6):
        voxel = Voxel((x, 0, z), texture=grass_texture)
    while t >= -10:
        for z in range(6):
            for x in range(6):
                voxel = Voxel((x, t, z), texture=soil_texture)
        t -= 1

player = FirstPersonController()
sky = Sky()
app.run()
