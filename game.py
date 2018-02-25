import sys
import math
import pygame
import colorsys
from collections import namedtuple


Vertex = namedtuple('Vertex', ['coords', 'faces'])
Face = namedtuple('Face', ['vertices', 'color'])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MENU_BGC = (19, 123, 58)

EQUILATERAL = math.sqrt(3) / 2
ISOCELES_RIGHT = 0.5


class Board:
    def __init__(self, x, y, width, height, a, tri=EQUILATERAL):
        # Using Face-Vertex mesh datastructure
        self.vertices = []
        self.faces = []

        h = tri * a
        a_half = a / 2
        v = [float(x), float(y)]

        # Generate vertices
        for row in range(1, height + 1):
            for col in range(width):
                self.vertices.append(Vertex(v, []))
                v = [v[0] + h, v[1] - a_half]
            v = [x + row * h, y + row * a_half]

        # Generate faces pointing to vertex array by index
        i = lambda row, col: col + row * width
        for r in range(height - 1):
            for c in range(width):
                if c - 1 >= 0:
                    face = [i(r, c), i(r + 1, c), i(r + 1, c - 1)]
                    self.faces.append(Face(face, ''))
                if c + 1 < width:
                    face = [i(r, c), i(r + 1, c), i(r, c + 1)]
                    self.faces.append(Face(face, ''))

        # For each vertex put a list of its neighbouring faces
        for i, face in enumerate(self.faces):
            for v in face.vertices:
                self.vertices[v].faces.append(i)

    def rotate(self, angle):
        a = self.vertices[0].coords
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for i, v in enumerate(self.vertices):
            b = v.coords
            vector = [b[0] - a[0], b[1] - a[1]]
            new_vector = [vector[0] * cos_angle - vector[1] * sin_angle,
                          vector[0] * sin_angle + vector[1] * cos_angle]
            new_pos = [a[0] + new_vector[0], a[1] + new_vector[1]]
            self.vertices[i] = Vertex(new_pos, self.vertices[i].faces)

    def vertex_neighbours(self, v):
        neighbours = []
        for f_ref in self.vertices[v].faces:
            for v_ref in self.faces[f_ref].vertices:
                if v_ref != i_vertex and v_ref not in neighbours:
                    neighbours.append(v_ref)
        return neighbours

    def vertex_coords(self, v):
        return self.vertices[v].coords

    def vertex_faces(self, v):
        return self.vertices[v].faces

    def faces_of_edge(self, v0, v1):
        return list(set(self.vertex_faces(v0)) & set(self.vertex_faces(v1)))

    def draw(self, surface):
        r = 5
        from random import randrange as rnd
        for triangle in self.faces:
            a = self.vertex_coords(triangle.vertices[0])
            b = self.vertex_coords(triangle.vertices[1])
            c = self.vertex_coords(triangle.vertices[2])
            pygame.draw.aalines(surface, WHITE, True, (a, b, c))
            #pygame.draw.polygon(surface, (rnd(255), rnd(255), rnd(255)), (a, b, c))

        for v in self.vertices:
            x, y = v.coords
            pygame.draw.ellipse(surface, BLUE, (x - r, y - r, 2 * r, 2 * r))


class Player:
    # move and occupy by clicking with bindings
    # animate move with lerp
    def __init__(self, x, y, a, color, smooth=10):
        self.pos = [x, y]
        self.r = int(a / math.sqrt(3))
        self.color = colorsys.rgb_to_hsv(*color)
        self.smooth = smooth
        self.texture = self.render_texture(a)

    def render_texture(self, x):
        r = self.r
        color = [self.color[0], self.color[1], 80]
        texture = pygame.Surface((r * 2, r * 2), flags=pygame.SRCALPHA)

        while r >= 0:
            a = (self.r - r, self.r + r)
            b = (self.r + r, self.r + r)
            c = (self.r, self.r - r)
            pygame.draw.polygon(texture, colorsys.hsv_to_rgb(*color), (a, b, c))
            r -= self.r / self.smooth
            color[2] += (255 - 80) / self.smooth
        return texture

    def draw(self, canvas):
        canvas.blit(self.texture, (self.pos[0] - self.r, self.pos[1] - self.r))


Button = namedtuple('Button', ['rect', 'slot'])
Signal = namedtuple('Signal', ['setup', 'events', 'draw'])

class Game:
    def __init__(self, width, height):
        self.fontfile = 'Triangles-Regular.otf'
        self.title = 'COUNTRY OF 3 VERTICES'
        self.width = width
        self.height = height
        self.intro_buttons = []
        pygame.init()
        self.canvas = pygame.display.set_mode((self.width, self.height),
                                              pygame.RESIZABLE)
        fieldsize = 60
        self.board = Board(20, self.height // 2, 8, 8, fieldsize)
        self.player = Player(20, self.height // 3, fieldsize // 2, GREEN)

    def font_optsize(self, text, relative):
        return int(2 * ((self.width * relative) / len(text)))

    def xmargin(self, surface, relative=0.5):
        return (self.width - surface.get_rect()[2]) * relative

    def ymargin(self, surface, relative=0.5):
        return (self.height - surface.get_rect()[3]) * relative

    def intro_layout_draw(self):
        fontsize = self.font_optsize(self.title, 0.7)
        font = pygame.font.Font(self.fontfile, fontsize)

        title = font.render(self.title, False, (255, 240, 0), MENU_BGC)
        play = font.render('PLAY', False, WHITE, MENU_BGC)
        guide = font.render('HOW TO', False, WHITE, MENU_BGC)

        self.canvas.fill(MENU_BGC)
        self.canvas.blit(title, (self.xmargin(title), self.ymargin(title, 0.1)))
        playsurf = self.canvas.blit(play, (self.xmargin(play),
                                           self.ymargin(play, 0.5)))

        a = Button(playsurf, Signal(None, None, self.gameplay))
        b = Button(self.canvas.blit(guide, (self.xmargin(guide),
                                    self.ymargin(guide, 0.7))), '')
        self.intro_buttons = [a, b]


    def intro_screen_events(self, event):
        LEFT = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                for button in self.intro_buttons:
                    if button.rect.collidepoint(event.pos):
                        return button.slot

        elif event.type == pygame.VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            pygame.display.set_mode(event.size, pygame.RESIZABLE)
            self.intro_layout_draw()


    def gameplay(self):
        self.canvas.fill(BLACK)
        self.board.draw(self.canvas)
        self.player.draw(self.canvas)

    def run(self, signals=None):
        signals = signals or Signal(self.intro_layout_draw,
                                    self.intro_screen_events,
                                    None)
        if signals.setup:
            signals.setup()

        while True:
            if signals.draw:
                signals.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if signals.events:
                    sig = signals.events(event)
                    if sig:
                        signals = sig
                        if signals.setup:
                            signals.setup()

            pygame.display.update()
            pygame.time.delay(30)

if __name__ == '__main__':
    game = Game(800, 500)
    game.run()
