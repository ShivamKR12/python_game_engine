import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
from physics import PhysicsEngine, RigidBody
from renderer import Renderer
from input_handler import InputHandler
from pyrr import Vector3, Matrix44
import numpy as np

class Camera:
    def __init__(self, position=Vector3([0.0, 0.0, 0.0]), up=Vector3([0.0, 1.0, 0.0]), yaw=-90.0, pitch=0.0):
        self.position = position
        self.front = Vector3([0.0, 0.0, -1.0])
        self.up = up
        self.right = Vector3([1.0, 0.0, 0.0])
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        self.renderer = Renderer(self.display)
        self.input_handler = InputHandler()
        self.physics_engine = PhysicsEngine()
        self.camera = Camera(Vector3([0, 70, 10]))

        self.rotation = [0, 0, 0]
        self.rigid_bodies = [
            RigidBody(Vector3([0, 0, 0])),
            RigidBody(Vector3([2, 0, 0]), dynamic=False)
        ]
        for body in self.rigid_bodies:
            body.load_model("assets/models/block.obj")
            self.physics_engine.add_object(body)

        self.texture_id = self.renderer.load_texture("assets/models/grass_block.png")
        self.font = pygame.font.SysFont('Arial', 18)

    def update(self):
        self.input_handler.handle_input(self.camera)
        self.physics_engine.update(0.01)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.renderer.shader_program)

        model_loc = glGetUniformLocation(self.renderer.shader_program, 'model')
        view_loc = glGetUniformLocation(self.renderer.shader_program, 'view')
        proj_loc = glGetUniformLocation(self.renderer.shader_program, 'projection')
        view_pos_loc = glGetUniformLocation(self.renderer.shader_program, 'viewPos')

        if model_loc == -1 or view_loc == -1 or proj_loc == -1 or view_pos_loc == -1:
            print("Error: Unable to find uniform locations")
            return

        view_matrix = Matrix44.look_at(
            self.camera.position, self.camera.position + self.camera.front, self.camera.up
        )
        projection_matrix = Matrix44.perspective_projection(45.0, self.display[0] / self.display[1], 0.1, 100.0)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, Matrix44.identity())
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection_matrix)
        glUniform3fv(view_pos_loc, 1, self.camera.position)

        for i in range(4):
            light_pos_loc = glGetUniformLocation(self.renderer.shader_program, f'lights[{i}].position')
            light_color_loc = glGetUniformLocation(self.renderer.shader_program, f'lights[{i}].color')
            if light_pos_loc == -1 or light_color_loc == -1:
                print(f"Error: Unable to find light uniform locations for light {i}")
                continue
            glUniform3fv(light_pos_loc, 1, Vector3(self.renderer.light_positions[i]))
            glUniform3fv(light_color_loc, 1, np.array(self.renderer.light_colors[i], dtype=np.float32))

        for body in self.rigid_bodies:
            self.renderer.draw_model(body.vao, body.vertex_count)

        self.renderer.render_text(f'Cube Position: {self.rigid_bodies[0].position}', (10, 130), self.font)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.update()
            self.render()
            pygame.time.wait(10)
        pygame.quit()

if __name__ == "__main__":
    engine = GameEngine(800, 600)
    engine.run()
