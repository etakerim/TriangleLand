import sys
import math
import pygame


def triangle_mesh(x, y, n, m, a):
    # h = a / 2                       # Isosceles right triangle
    h = (math.sqrt(3) * a) / 2        # Equilateral triangle
    a_half = a / 2
    vertex = [float(x), float(y)]
    mesh = []

    for i in range(1, n + 1):
        mesh.append([])
        for j in range(m):
            mesh[-1].append(vertex)
            vertex = [vertex[0] + h, vertex[1] - a_half]
        vertex = [x + i * h, y + i * a_half]

    return mesh

def find_masscentre(mesh):
    return [(mesh[0][0][0] + mesh[-1][-1][0]) / 2,
           (mesh[0][-1][1] + mesh[-1][0][1]) / 2]

def rotate_mesh(mesh, angle):
    mid = find_masscentre(mesh)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            vector = [mesh[i][j][0] - mid[0], mesh[i][j][1] - mid[1]]
            new_vector = [vector[0] * cos_angle - vector[1] * sin_angle,
                          vector[0] * sin_angle + vector[1] * cos_angle]
            mesh[i][j] = [mid[0] + new_vector[0], mid[1] + new_vector[1]]


def board_draw(surface, mesh):
    r = 5
    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            a = mesh[i][j]
            if i + 1 < len(mesh):
                pygame.draw.aaline(surface, WHITE, a, mesh[i + 1][j])
                if j - 1 >= 0:
                    pygame.draw.aaline(surface, WHITE, a, mesh[i + 1][j - 1])
            if j + 1 < len(mesh[i]):
                pygame.draw.aaline(surface, WHITE, a, mesh[i][j + 1])

            pygame.draw.ellipse(surface, BLUE,
                                (a[0] - r, a[1] - r, 2 * r, 2 * r))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

matrix = triangle_mesh(20, winsize[1] // 2, 8, 8, 50)
rotate_mesh(matrix, math.pi / 4)
# pprint(matrix)
board_draw(canvas, matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
