import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

# Define vertex data for a cube
cube_vertices = [
    (-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1),  # Front face
    (-1, -1, -1), (-1,  1, -1), ( 1,  1, -1), ( 1, -1, -1),  # Back face
    (-1,  1, -1), (-1,  1,  1), ( 1,  1,  1), ( 1,  1, -1),  # Top face
    (-1, -1, -1), ( 1, -1, -1), ( 1, -1,  1), (-1, -1,  1),  # Bottom face
    ( 1, -1, -1), ( 1,  1, -1), ( 1,  1,  1), ( 1, -1,  1),  # Right face
    (-1, -1, -1), (-1, -1,  1), (-1,  1,  1), (-1,  1, -1)   # Left face
]

# Define vertex indices for drawing the cube
cube_indices = [
    0,  1,  2,  0,  2,  3,  # Front face
    4,  5,  6,  4,  6,  7,  # Back face
    8,  9, 10,  8, 10, 11,  # Top face
   12, 13, 14, 12, 14, 15,  # Bottom face
   16, 17, 18, 16, 18, 19,  # Right face
   20, 21, 22, 20, 22, 23   # Left face
]

# Define normal vectors for each face of the cube
cube_normals = [
    ( 0,  0,  1), ( 0,  0, -1), ( 0,  1,  0),  # Front, Back, Top
    ( 0, -1,  0), ( 1,  0,  0), (-1,  0,  0)   # Bottom, Right, Left
]

class Cube:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.vertices = self.batch.add_indexed(24, GL_TRIANGLES, None, cube_indices,
                                               ('v3f/static', cube_vertices),
                                               ('n3f/static', cube_normals))
        self.position = [0, 0, 0]
        self.selected = False

    def draw(self):
        if self.selected:
            glColor3f(1, 0, 0)  # Selected color (red)
        else:
            glColor3f(1, 1, 1)  # Default color (white)
        self.batch.draw()

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Setup initial camera position
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = -5

        # Setup rotation angle
        self.rotation = 0

        # Setup input handling
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.mouse = [0, 0]
        self.objects = []

        # Create cube objects
        for i in range(5):
            cube = Cube()
            cube.position = [i * 2 - 4, 0, 0]
            self.objects.append(cube)

        # Compile shaders
        self.vertex_shader = """
        // Vertex shader code (as string)
        """
        self.fragment_shader = """
        // Fragment shader code (as string)
        """

        self.program = self.create_program(self.vertex_shader, self.fragment_shader)

        # Get uniform locations
        self.model_loc = glGetUniformLocation(self.program, "model")
        self.view_loc = glGetUniformLocation(self.program, "view")
        self.projection_loc = glGetUniformLocation(self.program, "projection")
        self.material_ambient_loc = glGetUniformLocation(self.program, "material.ambient")
        self.material_diffuse_loc = glGetUniformLocation(self.program, "material.diffuse")
        self.material_specular_loc = glGetUniformLocation(self.program, "material.specular")
        self.material_shininess_loc = glGetUniformLocation(self.program, "material.shininess")
        self.light_position_loc = glGetUniformLocation(self.program, "light.position")
        self.light_ambient_loc = glGetUniformLocation(self.program, "light.ambient")
        self.light_diffuse_loc = glGetUniformLocation(self.program, "light.diffuse")
        self.light_specular_loc = glGetUniformLocation(self.program, "light.specular")

    def create_program(self, vertex_shader_source, fragment_shader_source):
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        return program

    def set_uniforms(self):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view_matrix())
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_matrix())
        glUniform3fv(self.material_ambient_loc, 1, (1.0, 0.5, 0.31))  # Material ambient color
        glUniform3fv(self.material_diffuse_loc, 1, (1.0, 0.5, 0.31))  # Material diffuse color
        glUniform3fv(self.material_specular_loc, 1, (0.5, 0.5, 0.5))  # Material specular color
        glUniform1f(self.material_shininess_loc, 32.0)  # Material shininess
        glUniform3fv(self.light_position_loc, 1, (1.2, 1.0, 2.0))  # Light position
        glUniform3fv(self.light_ambient_loc, 1, (0.2, 0.2, 0.2))  # Light ambient color
        glUniform3fv(self.light_diffuse_loc, 1, (0.5, 0.5, 0.5))  # Light diffuse color
        glUniform3fv(self.light_specular_loc, 1, (1.0, 1.0, 1.0))  # Light specular color
        glUseProgram(0)

    def view_matrix(self):
        return np.array([[1, 0, 0, -self.camera_x],
                         [0, 1, 0, -self.camera_y],
                         [0, 0, 1, -self.camera_z],
                         [0, 0, 0, 1]], dtype=np.float32)

    def projection_matrix(self):
        aspect_ratio = self.width / self.height
        return np.array([[1.0 / aspect_ratio, 0, 0, 0],
                         [0, 1.0, 0, 0],
                         [0, 0, -2.0, -(self.camera_z + 2)],
                         [0, 0, 0, 1]], dtype=np.float32)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        self.set_uniforms()

        for obj in self.objects:
            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()

        self.rotation += 1

    def update(self, dt):
        pass

if __name__ == "__main__":
    window = GameWindow(width=800, height=600, caption="Phong Shading")
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
