import pygame
import random


class SteeringBehaviors:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.panicDistance:float = 100
        self.panicDistanceSq:float = self.panicDistance ** 2
        self.wanderRadius:float = 100
        self.wanderDistance:float = 30
        self.wanderJitter:float = 30
        self.wanderTarget = pygame.Vector2(0,0)


    def seek(self, target:pygame.Vector2) -> pygame.Vector2:
        desiredVelocity = (target - self.vehicle.Pos()).normalize() * self.vehicle.maxForce
        return desiredVelocity - self.vehicle.velocity


    def flee(self, target:pygame.Vector2) -> pygame.Vector2:      
        if target.distance_squared_to(self.vehicle.Pos()) > self.panicDistanceSq:
            return pygame.Vector2(0,0)
        
        desiredVelocity = (self.vehicle.Pos() - target).normalize() * self.vehicle.maxForce
        return desiredVelocity - self.vehicle.velocity
    

    def wander(self) -> pygame.Vector2:
        self.wanderTarget += pygame.Vector2(randomClamped() * self.wanderJitter, randomClamped() * self.wanderJitter)
        self.wanderTarget = self.wanderTarget.normalize()
        self.wanderTarget *= self.wanderRadius
        targetLocal = self.wanderTarget + pygame.Vector2(self.wanderDistance, 0)
        return targetLocal

    def calculate(self) -> pygame.Vector2:
        #return self.seek(pygame.Vector2(pygame.mouse.get_pos()))
        return self.wander()
                                            
def randomClamped() -> float:
    return random.random() * 2 - 1