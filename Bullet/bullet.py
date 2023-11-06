import pygame
import math
from typing import List
from Obstacles.obstacles import Obstacles
from Enemy.enemy import Enemy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.position = pygame.Vector2(x, y)
        self.radius = 4
        self.speed = 0.8
        self.color = (255, 255, 255)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def draw(self):
        self.update()
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)

    def update(self):
        self.position.x += self.dx
        self.position.y += self.dy

    def check_collide_with_obstacles(self, obstacles: List[Obstacles]):
        for obstacle in obstacles:
            if self.position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
                return True
        return False

    def is_out_of_border(self, width, height):
        return (self.position.x - self.radius < 0 and
                self.position.x + self.radius > width and
                self.position.y - self.radius < 0 and
                self.position.y + self.radius > height)

    def check_collide_with_enemy(self, enemies: List[Enemy]):
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.radius + enemy.radius:
                return True, enemies.index(enemy)
        return False, -1


