import sys
import math
import pygame
from pprint import pprint


def rhombus_mesh(x, y, n, m, a):
    h = (math.sqrt(3) * a) / 2
    a_half = a / 2
    vertex = (float(x), float(y))
    mesh = []

    for i in range(1, n + 1):
        mesh.append([])
        for j in range(m):
            mesh[-1].append(vertex)
            vertex = (vertex[0] + h, vertex[1] - a_half)
        vertex = (x + i * h, y + i * a_half)

    return mesh


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

pprint(rhombus_mesh(20, winsize[1] // 2, 8, 8, 50))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
