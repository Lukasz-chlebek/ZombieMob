import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.position = pygame.Vector2(x, y)
        self.radius = 20
        self.color = (255, 0, 0)
        self.speed = 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)

    def move(self, direction):
        if direction == 'LEFT':
            self.position.x -= self.speed
        elif direction == 'RIGHT':
            self.position.x += self.speed
        elif direction == 'UP':
            self.position.y -= self.speed
        elif direction == 'DOWN':
            self.position.y += self.speed
