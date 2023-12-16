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
        self.maxVelocity:float = 250
        self.maxForce:float = 800
        self.maxTrunRate:float = 10
        self.is_in_world = False
        self.neighbors = []
        self.max_dinstance_to_neighbor = 150
        self.max_dinstance_to_neighbor_sq = self.max_dinstance_to_neighbor ** 2
        self.is_attacking = False

        self.steering = SteeringBehaviors(self)


    def draw(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.position.x, self.position.y), self.radius)


    def attack(self):
        self.is_attacking = True
        for neighbor in self.neighbors:
            if not neighbor.is_attacking:
                neighbor.attack()
        self.color = (255, 255, 0)
        self.steering.weights = self.steering.attack_weights


    def find_neighbors(self):
        self.neighbors = []
        for enemy in globals.ENEMIES:
            if enemy is not self and self.position.distance_squared_to(enemy.position) <= self.max_dinstance_to_neighbor_sq:
                self.neighbors.append(enemy)

    def update(self, deltaTime:float) -> None:
        self.find_neighbors()
        acceleration = self.steering.calculate(deltaTime)
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
        for neighbor in self.neighbors:
            if neighbor is self:
                continue
            if self.position.distance_to(neighbor.position) <= self.radius + neighbor.radius and (neighbor.position - self.position).length()!=0:
               self.position = -(neighbor.position - self.position).normalize() * (self.radius + neighbor.radius) + neighbor.position
        for obstacle in globals.OBSTACLES:
            if self.position.distance_to(obstacle.position) <= self.radius + obstacle.radius:
               self.position = -(obstacle.position - self.position).normalize() * (self.radius + obstacle.radius) + obstacle.position

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


