import pygame
import math
from typing import List
import globals
from SteeringBehaviors.SteeringBehaviors import SteeringBehaviors


class Line(pygame.sprite.Sprite):
    def __init__(self, begin :pygame.Vector2, end: pygame.Vector2 ):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255,255,255)
        self.begin = begin
        self.end = end

    def draw(self) -> None:
        pygame.draw.line(globals.WORLD, (255, 255, 255), self.begin, self.end)
        pygame.draw.circle(globals.WORLD,(255,255,255), self.end, 3)




