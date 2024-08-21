import pygame
from pyrr import Vector3

class InputHandler:
    def __init__(self, mouse_sensitivity=0.1, movement_speed=0.05):
        self.mouse_sensitivity = mouse_sensitivity
        self.movement_speed = movement_speed
        self.last_mouse_pos = pygame.mouse.get_pos()

    def handle_input(self, camera):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.position += camera.front * self.movement_speed
        if keys[pygame.K_s]:
            camera.position -= camera.front * self.movement_speed
        if keys[pygame.K_a]:
            camera.position -= camera.right * self.movement_speed
        if keys[pygame.K_d]:
            camera.position += camera.right * self.movement_speed
        if keys[pygame.K_SPACE]:
            camera.position += camera.up * self.movement_speed
        if keys[pygame.K_LSHIFT]:
            camera.position -= camera.up * self.movement_speed

        mouse_pos = pygame.mouse.get_pos()
        dx, dy = mouse_pos[0] - self.last_mouse_pos[0], mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos

        camera.yaw += dx * self.mouse_sensitivity
        camera.pitch -= dy * self.mouse_sensitivity

        if camera.pitch > 89.0:
            camera.pitch = 89.0
        if camera.pitch < -89.0:
            camera.pitch = -89.0

        camera.update_camera_vectors()
