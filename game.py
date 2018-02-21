import sys
import math
import pygame

class TriangleMesh:

    EQUILATERAL = math.sqrt(3) / 2
    ISOCELES_RIGHT = 0.5

    def __init__(self, x, y, n, m, a, tri=EQUILATERAL):
        self.mesh = []

        h = tri * a
        a_half = a / 2
        vertex = [float(x), float(y)]

        for i in range(1, n + 1):
            self.mesh.append([])
            for j in range(m):
                self.mesh[-1].append(vertex)
                vertex = [vertex[0] + h, vertex[1] - a_half]
            vertex = [x + i * h, y + i * a_half]

    @property
    def mass_centre(self):
        return [(self.mesh[0][0][0] + self.mesh[-1][-1][0]) / 2,
               (self.mesh[0][-1][1] + self.mesh[-1][0][1]) / 2]

    def rotate(self, angle):
        a = self.mesh[0][0]
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for i in range(len(self.mesh)):
            for j in range(len(self.mesh[i])):
                vector = [self.mesh[i][j][0] - a[0], self.mesh[i][j][1] - a[1]]
                new_vector = [vector[0] * cos_angle - vector[1] * sin_angle,
                              vector[0] * sin_angle + vector[1] * cos_angle]
                self.mesh[i][j] = [a[0] + new_vector[0], a[1] + new_vector[1]]


    def board_draw(self, surface):
        r = 5
        for i in range(len(self.mesh)):
            for j in range(len(self.mesh[i])):
                a = self.mesh[i][j]
                if i + 1 < len(self.mesh):
                    pygame.draw.aaline(surface, WHITE, a, self.mesh[i + 1][j])
                    if j - 1 >= 0:
                        pygame.draw.aaline(surface, WHITE, a, self.mesh[i + 1][j - 1])
                if j + 1 < len(self.mesh[i]):
                    pygame.draw.aaline(surface, WHITE, a, self.mesh[i][j + 1])

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

m = TriangleMesh(20, winsize[1] // 2, 8, 8, 50)
# m.rotate(math.pi / 4)
m.board_draw(canvas)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
