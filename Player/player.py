import pygame
import math
from typing import List
from Obstacles.obstacles import Obstacles
from Bullet.bullet import Bullet
import globals

class Player(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen:pygame.surface = screen
        self.position:pygame.Vector2 = pygame.Vector2(x, y)
        self.radius:float = 20
        self.color = (0, 0, 255)
        self.speed:float = 500
        self.direction:pygame.Vector2 = pygame.Vector2(0, 0)


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)


    def set_direction(self, direction:pygame.Vector2) -> None:
        self.direction = direction


    def move(self, deltaTime:float) -> None:
        self.position += self.direction * self.speed * deltaTime

    def update(self, deltaTime:float) -> None:
        self.move(deltaTime)
        self.check_collide_with_border(deltaTime)
        self.check_collide_with_obstacles(deltaTime)


    def shoot(self, mouse_position: pygame.Vector2):
        direction = mouse_position - self.position
        angle = math.atan2(direction.y, direction.x)
        return Bullet(self.screen, self.position.x, self.position.y, angle)

    def check_collide_with_obstacles(self, deltaTime:float):
        for obstacle in globals.OBSTACLES:
            if self.position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
               self.position = -(obstacle.position - self.position).normalize() * (self.radius + obstacle.radius) + obstacle.position


    def check_collide_with_border(self, deltaTime):
        if self.position.x + self.radius > globals.WIDTH:
            self.position.x = globals.WIDTH - self.radius
        if self.position.y + self.radius > globals.HEIGHT:
            self.position.y = globals.HEIGHT - self.radius
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
        if self.position.y - self.radius < 0:
            self.position.y = self.radius