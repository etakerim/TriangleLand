import sys
import math
import pygame
import colorsys

EQUILATERAL = math.sqrt(3) / 2
ISOCELES_RIGHT = 0.5


class TriangleMesh:

    def __init__(self, x, y, n, m, a, tri=EQUILATERAL):
        self.vertex = []
        self.edges = []

        h = tri * a
        a_half = a / 2
        vertex = [float(x), float(y)]

        for i in range(1, n + 1):
            self.vertex.append([])
            for j in range(m):
                self.vertex[-1].append(vertex)
                vertex = [vertex[0] + h, vertex[1] - a_half]
            vertex = [x + i * h, y + i * a_half]

        for i in range(len(self.vertex)):
            for j in range(len(self.vertex[i])):
                pt = []
                if i + 1 < len(self.vertex):
                    pt.append([i + 1, j])
                    if j - 1 >= 0:
                        pt.append([i + 1, j - 1])
                if j + 1 < len(self.vertex[i]):
                    pt.append([i, j + 1])
                if pt:
                    self.edges.append(pt)


    @property
    def mass_centre(self):
        return [(self.vertex[0][0][0] + self.vertex[-1][-1][0]) / 2,
               (self.vertex[0][-1][1] + self.vertex[-1][0][1]) / 2]

    def rotate(self, angle):
        a = self.vertex[0][0]
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for i in range(len(self.vertex)):
            for j in range(len(self.vertex[i])):
                vector = [self.vertex[i][j][0] - a[0], self.vertex[i][j][1] - a[1]]
                new_vector = [vector[0] * cos_angle - vector[1] * sin_angle,
                              vector[0] * sin_angle + vector[1] * cos_angle]
                self.vertex[i][j] = [a[0] + new_vector[0], a[1] + new_vector[1]]


    def board_draw(self, surface):
        r = 5
        for i in range(len(self.vertex)):
            for j in range(len(self.vertex[i])):
                a = self.vertex[i][j]
                if i + 1 < len(self.vertex):
                    pygame.draw.aaline(surface, WHITE, a, self.vertex[i + 1][j])
                    if j - 1 >= 0:
                        pygame.draw.aaline(surface, WHITE, a, self.vertex[i + 1][j - 1])
                if j + 1 < len(self.vertex[i]):
                    pygame.draw.aaline(surface, WHITE, a, self.vertex[i][j + 1])

                pygame.draw.ellipse(surface, BLUE,
                                    (a[0] - r, a[1] - r, 2 * r, 2 * r))


class Player:
    # move and occupy by clicking with bindings
    # animate move with lerp
    def __init__(self, x, y, a, color, smooth=10):
        self.pos = [x, y]
        self.r = int(a / math.sqrt(3))
        self.color = colorsys.rgb_to_hsv(*color)
        self.smooth = smooth

    def draw(self, canvas):
        r = self.r
        color = [self.color[0], self.color[1], 80]

        while r >= 0:
            a = (self.pos[0] - r, self.pos[1] + r)
            b = (self.pos[0] + r, self.pos[1] + r)
            c = (self.pos[0], self.pos[1] - r)
            pygame.draw.polygon(canvas, colorsys.hsv_to_rgb(*color),
                                [a, b, c])
            r -= self.r / self.smooth
            color[2] += (255 - 80) / self.smooth


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

m = TriangleMesh(20, winsize[1] // 2, 8, 8, 60)
# m.rotate(math.pi / 4)
m.board_draw(canvas)
p = Player(100, 100, 60, GREEN)
p1 = Player(200, 100, 60, RED)
p2 = Player(300, 100, 60, BLUE)
p.draw(canvas)
p1.draw(canvas)
p2.draw(canvas)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
