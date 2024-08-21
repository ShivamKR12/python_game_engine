import pygame
from pygame.locals import *
from custom_physics import SimplePhysicsEngine, PhysicsObject

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Custom Physics Engine
physics = SimplePhysicsEngine()
player = PhysicsObject(mass=1.0, position=(400, 300, 0))
physics.add_object(player)

# Game loop
running = True
while running:
    delta_time = clock.tick(60) / 1000.0  # Time in seconds

    # Handle events
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player.apply_force((-1000, 0, 0), delta_time)
    if keys[K_RIGHT]:
        player.apply_force((1000, 0, 0), delta_time)
    if keys[K_UP]:
        player.apply_force((0, -1000, 0), delta_time)
    if keys[K_DOWN]:
        player.apply_force((0, 1000, 0), delta_time)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Update physics
    physics.update(delta_time)

    # Clear screen
    screen.fill(WHITE)

    # Draw player
    pygame.draw.circle(screen, RED, (int(player.position[0]), int(player.position[1])), 10)

    # Update display
    pygame.display.flip()

pygame.quit()
