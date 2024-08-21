import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *

class Renderer:
    def __init__(self, display):
        self.display = display
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 100.0)
        glTranslatef(0.0, 0.0, -5)
        glEnable(GL_DEPTH_TEST)
        self.shader_program = self.load_shader('shaders/vertex_shader.glsl', 'shaders/fragment_shader.glsl')
        self.init_lighting()

    def load_shader(self, vertex_path, fragment_path):
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

    def load_texture(self, path):
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

    def init_lighting(self):
        self.light_positions = [
            [10.0, 10.0, 10.0],
            [-10.0, 10.0, 10.0],
            [10.0, -10.0, 10.0],
            [-10.0, -10.0, 10.0]
        ]
        self.light_colors = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]

    def draw_model(self, vao, vertex_count):
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, vertex_count)
        glBindVertexArray(0)

    def render_text(self, text, position, font):
        text_surface = font.render(text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
