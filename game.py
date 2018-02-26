import sys
import pygame
from collections import namedtuple
from hud import MenuScreen
from board import Board
from player import Player
from patch import *


class Game:
    def __init__(self, width, height):
        game_name = 'COUNTRY OF 3 VERTICES'
        pygame.init()
        self.canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(game_name)
        self.menu = MenuScreen(self.canvas)
        fieldsize = 60
        self.board = Board(20, 300, 8, 8, fieldsize)
        self.player = Player(20, 300, fieldsize // 2, GREEN)

    def gameplay(self):
        self.canvas.fill(BLACK)
        self.board.draw(self.canvas)
        self.player.draw(self.canvas)

    def change_callbacks(self, orig, new):
        """ To have complete control over event loop - 'setup' and 'event' callbacks
        are able to modify state of loop callbacks by returning a new callback.
        The reasons are:
            - Events: they are self explanatory. When user clickes a button or
                      move / hover over something it usually changes what is
                      draw. -> Button on_click holds new loop callbacks
            - Setup: It usually calculates layout
                     or it can be used as proxy to change currently running
                     callbacks or animations.
        """
        if new:
            if new.setup:
                mod = new.setup()
                return self.change_callbacks(new, mod)
            else:
                return new
        else:
            return orig

    def run(self, callbacks=None):
        """ To have unified control over drawing pipeline 'run' function
            is calling signal callbacks - 'setup' once - 'events' and
            'draw' on every iteration
        """
        initcalls = Callbacks(self.menu.draw, self.menu.events, None)
        callbacks = callbacks or initcalls

        if callbacks.setup:
            callbacks.setup()

        while True:
            if callbacks.draw:
                callbacks.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if callbacks.events:
                    new = callbacks.events(event)
                    if new:
                        callbacks = self.change_callbacks(callbacks, new)

            pygame.display.update()
            pygame.time.delay(30)


if __name__ == '__main__':
    game = Game(800, 500)
    game.run()
