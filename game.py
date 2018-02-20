import sys
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

winsize = (800, 600)
pygame.init()
canvas = pygame.display.set_mode(winsize)

def rhombus(x_inc):
    r = 5
    a = [20, winsize[1] // 2]

    for i in range(1, 9):
        for y in range(8):
            pygame.draw.ellipse(canvas, BLUE, (a[0] - r, a[1] - r, 2*r, 2*r))
            a = [a[0] + x_inc, a[1] - 25]
        a = [20 + i * x_inc, (winsize[1] // 2) + i * 25]


rhombus(50)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(30)
