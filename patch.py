import pygame
import sys
from collections import namedtuple


def terminate(event=None):
    pygame.quit()
    sys.exit()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_name = 'COUNTRY OF 3 VERTICES'
Callbacks = namedtuple('Callbacks', ['setup', 'events', 'draw'])
