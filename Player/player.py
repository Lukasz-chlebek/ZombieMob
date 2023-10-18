import pygame
import math
from typing import List
from Obstacles.obstacles import Obstacles


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

    def check_collide_with_obstacles(self, obstacles: List[Obstacles], x, y):
        for obstacle in obstacles:
            temp_position = pygame.Vector2(self.position.x + x, self.position.y + y)
            if temp_position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
                return True
        return False

    def is_not_out_of_border(self, width, height, x, y):
        temp_position = pygame.Vector2(self.position.x + x, self.position.y + y)
        return (temp_position.x - self.radius >= 0 and
                temp_position.x + self.radius <= width and
                temp_position.y - self.radius >= 0 and
                temp_position.y + self.radius <= height)
