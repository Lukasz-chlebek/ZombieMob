import pygame
from typing import List

from line import Line
from Player.player import Player
from Obstacles.obstacles import Obstacles
from Bullet.bullet import Bullet
from Enemy.enemy import Enemy


WIDTH = 1080
HEIGHT = 720
BACKGROUND = (0, 0, 0)
FPS = 40
WORLD = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER = Player(WORLD, WIDTH // 2, HEIGHT // 2)
CLOCK = pygame.time.Clock()
OBSTACLES_LIMIT = 5
OBSTACLES:List[Obstacles] = []
BULLETS:List[Bullet] = []
ENEMIES:List[Enemy] = [Enemy(WORLD, WIDTH//2, HEIGHT//2)]
lines:List[Line] =[]


def clear_lines():
    global lines
    lines = []