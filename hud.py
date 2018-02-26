import pygame
from player import Player
from patch import *


class Button:
    def __init__(self, rect, callback):
        self.rect = rect
        self.on_click = callback


class Piece:
    def __init__(self, is_selected, color, player, rect=0):
        self.is_selected = is_selected
        self.color = color
        self.player = player
        self.rect = rect


class MenuScreen:
    BGCOLOR = (19, 123, 58)
    HEADING_COLOR = (255, 240, 0)
    CONTAINER_BORDER = (172, 172, 172)
    CONTAINER_COLOR = (47, 19, 4)

    def __init__(self, canvas):
        self.buttons = [
            Button(None, Callbacks(self.activate_select, self.events, None)),
            Button(None, Callbacks(terminate, None, None))
        ]
        self.yrel_pos = [0.1, 0.5, 0.7]
        self.fontfile = 'Triangles-Regular.otf'
        self.canvas = canvas
        self.figpool = False
        self.fig_refframe = pygame.Rect(0, 0, 0, 0)
        self.pieces = [Piece(False, RED, None),
                       Piece(False, GREEN, None),
                       Piece(False, self.HEADING_COLOR, None),
                       Piece(False, WHITE, None)]

    def font_optsize(self, text, relative):
        return int(2 * ((self.canvas.get_rect()[2] * relative) / len(text)))

    def xmargin(self, surface, relative=0.5):
        return (self.canvas.get_rect()[2] - surface.get_rect()[2]) * relative

    def ymargin(self, surface, relative=0.5):
        return (self.canvas.get_rect()[3] - surface.get_rect()[3]) * relative

    def draw(self):
        fontsize = self.font_optsize(game_name, 0.7)
        font = pygame.font.Font(self.fontfile, fontsize)

        title = font.render(game_name, False, self.HEADING_COLOR, self.BGCOLOR)
        play = font.render('PLAY', False, WHITE, self.BGCOLOR)
        quit = font.render('QUIT', False, WHITE, self.BGCOLOR)
        elements = [title, play, quit]

        self.canvas.fill(self.BGCOLOR)
        surfaces = []
        for yrel, btn in zip(self.yrel_pos, elements):
            pos = (self.xmargin(btn), self.ymargin(btn, yrel))
            surface = self.canvas.blit(btn, pos)
            surfaces.append(surface)

        if self.figpool:
            self.pieces_picker(surfaces)

        self.buttons[0].rect = surfaces[1]
        self.buttons[1].rect = surfaces[2]

    def events(self, event):
        LEFT = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        # Nemôžem active_select robiť tu?
                        return button.on_click
                if self.figpool:
                    for piece in self.pieces:
                        # Recalculte rect based on canvas reference frame not
                        # container
                        rrr = piece.player.texture.get_rect()
                        rrr[0] = self.fig_refframe[0] + piece.rect[0]
                        rrr[1] = self.fig_refframe[1] + piece.rect[1]
                        if rrr.collidepoint(event.pos):
                            piece.is_selected = not piece.is_selected
                            self.draw()

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.set_mode(event.size, pygame.RESIZABLE)
            self.draw()

    def activate_select(self):
        self.figpool = True
        self.yrel_pos = [0.1, 0.4, 0.9]
        self.buttons[0].on_click = Callbacks(None, None, None)
        # gameplay, gameevents, None)
        return Callbacks(self.draw, self.events, None)

    def pieces_picker(self, surfaces):
        fontsmall = pygame.font.Font(self.fontfile,
                                self.font_optsize(game_name, 0.3))

        pieces_container = pygame.Surface((surfaces[0][2],
                    abs(surfaces[2][1] - 1.2 * surfaces[2][3] - surfaces[1][1])))

        hint = fontsmall.render('CHOOSE GAME PIECES', False, WHITE, self.CONTAINER_COLOR)

        pieces_container.fill(self.CONTAINER_COLOR)
        pieces_container.blit(hint, (5, 5))
        figspc = pieces_container.get_rect()[2] // 4
        xpad = figspc // 2
        figwidth = figspc // 2
        ybottom = pieces_container.get_rect()[3] * 0.6
        for i, piece in enumerate(self.pieces):
            if piece.is_selected:
                al = 255
            else:
                al = 100
            piece.player = Player(i * figspc + xpad, ybottom, figwidth,
                                  piece.color, al)
            piece.rect = piece.player.draw(pieces_container)

        pygame.draw.rect(pieces_container, self.CONTAINER_BORDER, pieces_container.get_rect(), 3)
        self.fig_refframe = self.canvas.blit(pieces_container, (surfaces[0][0], surfaces[1][1] + surfaces[1][3] + 5))
