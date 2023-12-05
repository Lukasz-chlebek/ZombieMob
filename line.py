import pygame
import math
from typing import List
import globals
from SteeringBehaviors.SteeringBehaviors import SteeringBehaviors


class Line(pygame.sprite.Sprite):
    def __init__(self, begin :pygame.Vector2, end: pygame.Vector2, color = (255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.begin = begin
        self.end = end

    def draw(self) -> None:
        pygame.draw.line(globals.WORLD, self.color, self.begin, self.end)
        pygame.draw.circle(globals.WORLD,self.color, self.end, 3)




