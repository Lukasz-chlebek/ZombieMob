import pygame
from typing import List

import Obstacles.obstacles
import line
import Player.player
import Bullet.bullet
import Enemy.enemy

SCORE = 0
BEST_SCORE = 0
WIDTH = 1080
HEIGHT = 720
BACKGROUND = (0, 0, 0)
FOREGROUND = (255, 255, 255)
FPS = 40
WORLD = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER = Player.player.Player(WORLD, WIDTH // 2, HEIGHT // 2)
CLOCK = pygame.time.Clock()
OBSTACLES_LIMIT = 8
ENEMIES_LIMIT = 1
OBSTACLES:List[Obstacles.obstacles.Obstacles] = []
BULLETS:List[Bullet.bullet.Bullet] = []
ENEMIES:List[Enemy.enemy.Enemy] = []
lines:List[line.Line] =[]
debug_draw = False



def clear_lines():
    global lines
    lines = []