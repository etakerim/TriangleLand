import sys
import math
import pygame


def rhombus_mesh(x, y, n, m, a):
    r = 5
    h = (math.sqrt(3) * a) / 2
    a_half = a / 2
    vertex = (x, y)

    for i in range(1, n + 1):
        for j in range(m):
            pygame.draw.ellipse(canvas, BLUE,
                                (vertex[0] - r, vertex[1] - r, 2 * r, 2 * r))
            vertex = (vertex[0] + h, vertex[1] - a_half)
        vertex = (x + i * h, y + i * a_half)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

rhombus_mesh(20, winsize[1] // 2, 8, 8, 50)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
