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


Button = namedtuple('Button', ['rect', 'callback'])
Signal = namedtuple('Signal', ['setup', 'events', 'draw'])

def terminate(event=None):
    pygame.quit()
    sys.exit()


class MenuScreen:
    BGCOLOR = (19, 123, 58)
    HEADING_COLOR = (255, 240, 0)
    CONTAINER_BORDER = (172, 172, 172)
    CONTAINER_COLOR = (47, 19, 4)

    def __init__(self, canvas):
        self.buttons = []
        self.yrel_pos = [0.1, 0.5, 0.7]
        self.fontfile = 'Triangles-Regular.otf'
        self.canvas = canvas

    def font_optsize(self, text, relative):
        return int(2 * ((self.canvas.get_rect()[2] * relative) / len(text)))

    def xmargin(self, surface, relative=0.5):
        return (self.canvas.get_rect()[2] - surface.get_rect()[2]) * relative

    def ymargin(self, surface, relative=0.5):
        return (self.canvas.get_rect()[3] - surface.get_rect()[3]) * relative

    def draw(self):
        title = 'COUNTRY OF 3 VERTICES'
        fontsize = self.font_optsize(title, 0.7)
        font = pygame.font.Font(self.fontfile, fontsize)

        title = font.render(title, False, self.HEADING_COLOR, self.BGCOLOR)
        play = font.render('PLAY', False, WHITE, self.BGCOLOR)
        quit = font.render('QUIT', False, WHITE, self.BGCOLOR)
        elements = [title, play, quit]

        self.canvas.fill(self.BGCOLOR)
        self.surfaces = []
        for yrel, btn in zip(self.yrel_pos, elements):
            pos = (self.xmargin(btn), self.ymargin(btn, yrel))
            surface = self.canvas.blit(btn, pos)
            self.surfaces.append(surface)

        self.buttons = [
            Button(self.surfaces[1], Signal(self.draw, self.events, None)),
            Button(self.surfaces[2], Signal(terminate, None, None))
        ]

    def events(self, event):
        LEFT = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        return button.callback

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.set_mode(event.size, pygame.RESIZABLE)
            self.draw()

    def pieces_picker(self, surfaces):
        fontsmall = pygame.font.Font(self.fontfile,
                                self.font_optsize(self.title, 0.3))

        self.yrel_pos = [0.1, 0.4, 0.9]
        pieces_container = pygame.Surface((surfaces[0][2],
                    abs(surfaces[2][1] - 1.2 * surfaces[2][3] - surfaces[1][1])))

        hint = fontsmall.render('CHOOSE GAME PIECES', False, WHITE, self.CONTAINER_COLOR)

        pieces_container.fill(MENU_CONTAINER_COLOR)
        pieces_container.blit(hint, (5, 5))
        figspc = pieces_container.get_rect()[2] // 4
        xpad = figspc // 2
        figwidth = figspc // 2
        ybottom = pieces_container.get_rect()[3] * 0.6
        pieces = [Player(0 * figspc + xpad, ybottom, figwidth, RED),
                    Player(1 * figspc + xpad, ybottom, figwidth, GREEN),
                    Player(2 * figspc + xpad, ybottom, figwidth, BLUE),
                    Player(3 * figspc + xpad , ybottom, figwidth, WHITE)]
        for piece in pieces:
            piece.draw(pieces_container)
        pygame.draw.rect(pieces_container, self.CONTAINER_BORDER, pieces_container.get_rect(), 3)
        self.canvas.blit(pieces_container, (surfaces[0][0], surfaces[1][1] + surfaces[1][3] + 5))

        # a = Button(playsurf, Signal(None, None, gameplay))
        # b = Button(guidesurf, Signal(terminate, None, None))
        self.buttons = [a, b]


class Game:
    def __init__(self, width, height):
        self.title = 'COUNTRY OF 3 VERTICES'
        pygame.init()
        self.canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        self.menu = MenuScreen(self.canvas)
        fieldsize = 60
        self.board = Board(20, 300, 8, 8, fieldsize)
        self.player = Player(20, 300, fieldsize // 2, GREEN)

    def gameplay(self):
        self.canvas.fill(BLACK)
        self.board.draw(self.canvas)
        self.player.draw(self.canvas)

    def run(self, signal=None):
        initsig = Signal(self.menu.draw, self.menu.events, None)
        signal = signal or initsig

        if signal.setup:
            signal.setup()

        while True:
            if signal.draw:
                signal.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if signal.events:
                    sig = signal.events(event)
                    if sig:
                        signal = sig
                        if signal.setup:
                            signal.setup()

            pygame.display.update()
            pygame.time.delay(30)

if __name__ == '__main__':
    game = Game(800, 500)
    game.run()
