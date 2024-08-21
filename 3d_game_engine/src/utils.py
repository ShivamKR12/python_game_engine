import numpy as np
import ctypes
from OpenGL.GL import *
import pygame

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    # Check for compilation errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(f"Shader compilation failed: {error}")
        glDeleteShader(shader)
        return None
    
    return shader

def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    
    if vertex_shader is None or fragment_shader is None:
        return None
    
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    
    # Check for linking errors
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        print(f"Shader program linking failed: {error}")
        glDeleteProgram(program)
        return None
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

def load_shader(vertex_path, fragment_path):
    with open(vertex_path, 'r') as f:
        vertex_src = f.read()
    with open(fragment_path, 'r') as f:
        fragment_src = f.read()
    
    return create_shader_program(vertex_src, fragment_src)


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
    vertices = np.array(vertices, dtype=np.float32)  # Ensure vertices is a numpy array
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

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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
