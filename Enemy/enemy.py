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
        self.radius:float = 20
        self.color = (255, 0, 0)
        self.velocity:pygame.Vector2 = pygame.Vector2()
        self.heading:pygame.Vector2 = pygame.Vector2()
        self.side:pygame.Vector2 = pygame.Vector2()
        self.mass:float = 1
        self.maxVelocity:float = 200
        self.maxForce:float = 800
        self.maxTrunRate:float = 10
        self.steering = SteeringBehaviors(self)
        

    def draw(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)

    def update(self, deltaTime:float) -> None:
        acceleration = self.steering.calculate()
        self.velocity += acceleration * deltaTime
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(self.maxVelocity)
        self.position += self.velocity * deltaTime
        if self.position.x < 0:
            self.position.x = globals.WIDTH
        if self.position.x > globals.WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = globals.HEIGHT
        if self.position.y > globals.HEIGHT:
            self.position.y = 0
        pass

    def Pos(self) -> pygame.Vector2:
        return self.position


