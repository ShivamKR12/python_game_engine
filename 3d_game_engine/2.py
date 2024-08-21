from OpenGL.GL import *
import numpy as np
from pyrr import Matrix44, Vector3
from src.renderer import load_shader, load_model_from_file, draw_model, load_texture
from src.objects import Camera
from src.physics import RigidBody, GRAVITY, detect_collision
from src.renderer import create_shadow_map
import pygame

class GameEngine:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        self.shader_program = load_shader('shaders/vertex_shader.glsl', 'shaders/fragment_shader.glsl')

        # Load complex model and texture
        self.vao_list, self.vertex_counts, self.textures = load_model_from_file('assets/models/House_Complex/House_Complex.obj')

        # Initialize the camera at a higher position
        self.camera = Camera(position=Vector3([0, 70, 10]))

        self.model = Matrix44.identity()
        self.projection = Matrix44.perspective_projection(45.0, 800 / 600, 0.1, 100.0)

        self.camera_speed = 0.1
        self.last_mouse_x, self.last_mouse_y = pygame.mouse.get_pos()
        self.mouse_sensitivity = 0.1

        self.light_positions = [
            Vector3([2.0, 4.0, 1.0]),
            Vector3([-2.0, 4.0, -1.0]),
            Vector3([2.0, -4.0, 1.0]),
            Vector3([-2.0, -4.0, -1.0])
        ]
        self.light_colors = [
            np.array([1.0, 1.0, 1.0], dtype=np.float32),
            np.array([1.0, 1.0, 1.0], dtype=np.float32),
            np.array([1.0, 1.0, 1.0], dtype=np.float32),
            np.array([1.0, 1.0, 1.0], dtype=np.float32)
        ]

        self.shadow_map_fbo, self.shadow_map = create_shadow_map(1024, 1024)
        self.rigid_bodies = []

        # Add a rigid body for the model
        self.rigid_bodies.append(RigidBody(Vector3([0, 0, 0])))

    def update(self):
        delta_time = 1 / 60.0  # Assuming a fixed time step for simplicity

        # Apply physics
        for body in self.rigid_bodies:
            body.apply_force(GRAVITY * body.mass)
            body.update(delta_time)

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.move(Vector3([0, 0, -self.camera_speed]))
        if keys[pygame.K_s]:
            self.camera.move(Vector3([0, 0, self.camera_speed]))
        if keys[pygame.K_a]:
            self.camera.move(Vector3([-self.camera_speed, 0, 0]))
        if keys[pygame.K_d]:
            self.camera.move(Vector3([self.camera_speed, 0, 0]))

        # Handle mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = (mouse_x - self.last_mouse_x) * self.mouse_sensitivity
        dy = (self.last_mouse_y - mouse_y) * self.mouse_sensitivity
        self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

        self.camera.rotate(dx, dy)

    def render(self):
        glUseProgram(self.shader_program)

        model_loc = glGetUniformLocation(self.shader_program, 'model')
        view_loc = glGetUniformLocation(self.shader_program, 'view')
        proj_loc = glGetUniformLocation(self.shader_program, 'projection')
        view_pos_loc = glGetUniformLocation(self.shader_program, 'viewPos')

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, self.model)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, self.camera.get_view_matrix())
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, self.projection)
        glUniform3fv(view_pos_loc, 1, self.camera.position)

        for i in range(4):
            light_pos_loc = glGetUniformLocation(self.shader_program, f'lights[{i}].position')
            light_color_loc = glGetUniformLocation(self.shader_program, f'lights[{i}].color')
            glUniform3fv(light_pos_loc, 1, self.light_positions[i])
            glUniform3fv(light_color_loc, 1, self.light_colors[i])

        for vao, vertex_count, texture in zip(self.vao_list, self.vertex_counts, self.textures):
            if texture:
                glBindTexture(GL_TEXTURE_2D, texture)
            draw_model(vao, vertex_count)
            glBindTexture(GL_TEXTURE_2D, 0)

        glUseProgram(0)

from OpenGL.GL import *
import pygame
import numpy as np
import ctypes
from src.utils import load_obj

def load_shader(vertex_path, fragment_path):
    with open(vertex_path, 'r') as f:
        vertex_src = f.read()
    with open(fragment_path, 'r') as f:
        fragment_src = f.read()

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_src)
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vertex_shader))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_src)
    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fragment_shader))

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader_program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

def load_model(vertices):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(5 * vertices.itemsize))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

def draw_model(vao, vertex_count):
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, vertex_count)
    glBindVertexArray(0)

def load_texture(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Load image
    image = pygame.image.load(path)
    image = pygame.transform.flip(image, False, True)
    img_data = pygame.image.tostring(image, "RGBA")

    width, height = image.get_rect().size
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture

def load_model_from_file(file_path):
    material_faces, material_dict = load_obj(file_path)
    vao_list = []
    vertex_counts = []
    textures = []

    for material, vertices in material_faces.items():
        vao = load_model(np.array(vertices, dtype=np.float32))
        vao_list.append(vao)
        vertex_counts.append(len(vertices) // 8)

        texture_file = material_dict[material]['texture'] if material in material_dict else None
        texture = load_texture(f"{file_path.rsplit('/', 1)[0]}/{texture_file}") if texture_file else None
        textures.append(texture)

    return vao_list, vertex_counts, textures

def create_shadow_map(width, height):
    depth_map_fbo = glGenFramebuffers(1)
    depth_map = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32))
    
    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    return depth_map_fbo, depth_map

def render_scene():
    # Render scene with shadow mapping
    pass

from pyrr import Matrix44, Vector3, vector
import numpy as np

class Camera:
    def __init__(self, position=Vector3([0, 0, 3]), target=Vector3([0, 0, 0]), up=Vector3([0, 1, 0])):
        self.position = position
        self.target = target
        self.up = up
        self.view_matrix = Matrix44.look_at(self.position, self.target, self.up)
        self.yaw = -90.0  # Facing forward in the -Z direction
        self.pitch = -30.0  # Slight downward angle

    def get_view_matrix(self):
        return self.view_matrix

    def move(self, direction):
        self.position += direction
        self.update_view_matrix()

    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch = max(-89.0, min(89.0, self.pitch + pitch))  # Limit pitch to avoid gimbal lock
        self.update_view_matrix()

    def update_view_matrix(self):
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.target = self.position + vector.normalize(front)
        self.view_matrix = Matrix44.look_at(self.position, self.target, self.up)

import numpy as np
from pyrr import Vector3

GRAVITY = Vector3([0, -9.81, 0])

class RigidBody:
    def __init__(self, position, mass=1.0, size=Vector3([1.0, 1.0, 1.0])):
        self.position = position
        self.velocity = Vector3([0, 0, 0])
        self.mass = mass
        self.size = size

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self, delta_time):
        self.position += self.velocity * delta_time

def detect_collision(obj1, obj2):
    # Simple AABB collision detection
    min1 = obj1.position - obj1.size / 2
    max1 = obj1.position + obj1.size / 2
    min2 = obj2.position - obj2.size / 2
    max2 = obj2.position + obj2.size / 2

    return (min1.x <= max2.x and max1.x >= min2.x and
            min1.y <= max2.y and max1.y >= min2.y and
            min1.z <= max2.z and max1.z >= min2.z)

import numpy as np

def load_obj(file_path):
    vertices = []
    textures = []
    normals = []
    faces = []
    material_dict = {}
    current_material = None

    def load_mtl(mtl_file_path):
        materials = {}
        current_material = None
        with open(mtl_file_path, 'r') as f:
            for line in f:
                if line.startswith('newmtl'):
                    current_material = line.split()[1]
                    materials[current_material] = {'texture': None}
                elif line.startswith('map_Kd'):
                    if current_material:
                        materials[current_material]['texture'] = line.split()[1]
        return materials

    obj_dir = '/'.join(file_path.split('/')[:-1])
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith('vt '):
                textures.append(list(map(float, line.strip().split()[1:3])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith('f '):
                face = []
                for v in line.strip().split()[1:]:
                    face.append(list(map(int, v.split('/'))))
                faces.append((face, current_material))
            elif line.startswith('mtllib'):
                mtl_file = line.split()[1]
                material_dict = load_mtl(f"{obj_dir}/{mtl_file}")
            elif line.startswith('usemtl'):
                current_material = line.split()[1]

    vertex_data = []
    material_faces = {}
    for face, material in faces:
        if material not in material_faces:
            material_faces[material] = []
        for v in face:
            vertex = vertices[v[0] - 1]
            tex = textures[v[1] - 1] if len(v) > 1 and v[1] else [0, 0]
            norm = normals[v[2] - 1] if len(v) > 2 and v[2] else [0, 0, 0]
            material_faces[material].extend(vertex + tex + norm)

    return material_faces, material_dict

#version 330 core
out vec4 FragColor;

in vec2 TexCoords;
in vec3 FragPos;
in vec3 Normal;

uniform sampler2D texture1;

struct Light {
    vec3 position;
    vec3 color;
};

uniform Light lights[4]; // Support up to 4 lights
uniform vec3 viewPos;

void main()
{
    vec3 ambient = 0.1 * vec3(texture(texture1, TexCoords));
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    vec3 result = ambient;

    for (int i = 0; i < 4; ++i) {
        vec3 lightDir = normalize(lights[i].position - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * vec3(texture(texture1, TexCoords));

        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = lights[i].color * spec;

        result += (diffuse + specular) * lights[i].color;
    }

    FragColor = vec4(result, 1.0);
}


#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normal;

out vec2 TexCoords;
out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = mat3(transpose(inverse(model))) * normal;
    TexCoords = texCoords;
    gl_Position = projection * view * model * vec4(position, 1.0);
}

import pygame
from OpenGL.GL import *
from src.game_engine import GameEngine

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption('3D Game Engine')
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    glClearColor(0.1, 0.1, 0.1, 1.0)
    

    engine = GameEngine()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        engine.update()
        engine.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
