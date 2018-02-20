import sys
import pygame

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
