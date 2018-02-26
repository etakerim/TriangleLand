import math
import pygame
import colorsys


class Player:
    # move and occupy by clicking with bindings
    # animate move with lerp
    def __init__(self, x, y, a, color, alpha=255, smooth=10):
        self.pos = [x, y]
        self.r = int(a / math.sqrt(3))
        self.color = colorsys.rgb_to_hsv(*color)
        self.render_texture(alpha, smooth)

    def render_texture(self, alpha, smooth=10):
        r = self.r
        color = [self.color[0], self.color[1], 80]
        texture = pygame.Surface((r * 2, r * 2), flags=pygame.SRCALPHA)

        while r >= 0:
            a = (self.r - r, self.r + r)
            b = (self.r + r, self.r + r)
            c = (self.r, self.r - r)
            pygame.draw.polygon(texture, (*colorsys.hsv_to_rgb(*color), alpha), (a, b, c))
            r -= self.r / smooth
            color[2] += (255 - 80) / smooth
        self.texture = texture

    def draw(self, canvas):
        return canvas.blit(self.texture, (self.pos[0] - self.r, self.pos[1] - self.r))
