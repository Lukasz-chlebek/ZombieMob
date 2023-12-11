import pygame
from typing import List

import Obstacles.obstacles
import line
import Player.player
import Bullet.bullet
import Enemy.enemy


WIDTH = 1080
HEIGHT = 720
BACKGROUND = (0, 0, 0)
FPS = 40
WORLD = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER = Player.player.Player(WORLD, WIDTH // 2, HEIGHT // 2)
CLOCK = pygame.time.Clock()
OBSTACLES_LIMIT = 8
ENEMIES_LIMIT = 50
OBSTACLES:List[Obstacles.obstacles.Obstacles] = []
BULLETS:List[Bullet.bullet.Bullet] = []
ENEMIES:List[Enemy.enemy.Enemy] = []
lines:List[line.Line] =[]


def clear_lines():
    global lines
    lines = []