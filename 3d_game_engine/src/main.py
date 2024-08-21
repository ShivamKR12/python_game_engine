import pygame
from OpenGL.GL import *
from game_engine import GameEngine

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption('3D Game Engine')
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    engine = GameEngine(800, 600)
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
