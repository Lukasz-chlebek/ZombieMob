import pygame
import math
from typing import List
import globals
from SteeringBehaviors.SteeringBehaviors import SteeringBehaviors


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.surface, x:float, y:float):
        pygame.sprite.Sprite.__init__(self)
        self.screen:pygame.surface = screen
        self.position:pygame.Vector2 = pygame.Vector2(x, y)
        self.radius:float = 6
        self.color = (255, 0, 0)
        self.velocity:pygame.Vector2 = pygame.Vector2()
        self.heading:pygame.Vector2 = pygame.Vector2()
        self.side:pygame.Vector2 = pygame.Vector2()
        self.mass:float = 1
        self.maxVelocity:float = 400
        self.maxForce:float = 800
        self.maxTrunRate:float = 10
        self.steering = SteeringBehaviors(self)
        self.is_in_world = False
        

    def draw(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)

    def update(self, deltaTime:float) -> None:
        acceleration = self.steering.calculate()
        self.velocity += acceleration * deltaTime
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(self.maxVelocity)
        self.position += self.velocity * deltaTime
        
        if self.velocity.length() != 0:
            self.heading = self.velocity.normalize()
        self.checkIfISInWorld()
        self.checkCollisionWithEntities()
        if self.is_in_world:
            self.checkCollisionWithWalls()
        
    def checkCollisionWithEntities(self):
        for obstacle in globals.OBSTACLES:
            if self.position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
               self.position = -(obstacle.position - self.position).normalize() * (self.radius + obstacle.radius) + obstacle.position
        for enemy in globals.ENEMIES:
            if enemy is self:
                continue
            if self.position.distance_to(enemy.position) <= self.radius + enemy.radius and (enemy.position - self.position).length()!=0:
               self.position = -(enemy.position - self.position).normalize() * (self.radius + enemy.radius) + enemy.position


    def checkCollisionWithWalls(self):
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
        if self.position.x + self.radius> globals.WIDTH:
            self.position.x = globals.WIDTH - self.radius
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
        if self.position.y + self.radius > globals.HEIGHT:
            self.position.y = globals.HEIGHT - self.radius

    def checkIfISInWorld(self):
        self.is_in_world = 0 < self.position.x < globals.WIDTH and 0 < self.position.y < globals.HEIGHT

    def Pos(self) -> pygame.Vector2:
        return self.position


