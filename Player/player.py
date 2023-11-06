import pygame
import math
from typing import List
from Obstacles.obstacles import Obstacles
from Bullet.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen:pygame.surface = screen
        self.position:pygame.Vector2 = pygame.Vector2(x, y)
        self.radius:float = 20
        self.color = (0, 0, 255)
        self.speed:float = 0.4

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)

    def move(self, direction:str):
        if direction == 'LEFT':
            self.position.x -= self.speed
        elif direction == 'RIGHT':
            self.position.x += self.speed
        elif direction == 'UP':
            self.position.y -= self.speed
        elif direction == 'DOWN':
            self.position.y += self.speed

    def shoot(self, mouse_position: pygame.Vector2):
        direction = mouse_position - self.position
        angle = math.atan2(direction.y, direction.x)
        return Bullet(self.screen, self.position.x, self.position.y, angle)

    def check_collide_with_obstacles(self, obstacles: List[Obstacles], x:float, y:float):
        for obstacle in obstacles:
            temp_position = pygame.Vector2(self.position.x + x, self.position.y + y)
            if temp_position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
                return True
        return False

    def is_not_out_of_border(self, width:float, height:float, x:float, y:float):
        temp_position = pygame.Vector2(self.position.x + x, self.position.y + y)
        return (temp_position.x - self.radius >= 0 and
                temp_position.x + self.radius <= width and
                temp_position.y - self.radius >= 0 and
                temp_position.y + self.radius <= height)
