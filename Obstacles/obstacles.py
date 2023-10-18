import pygame


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = (0, 255, 100)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)


