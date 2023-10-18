import pygame
import random
from typing import List

from Player.player import Player
from Obstacles.obstacles import Obstacles

WIDTH = 1280
HEIGHT = 960
BACKGROUND = (0, 0, 0)
FPS = 40
WORLD = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER = Player(WORLD, WIDTH // 2, HEIGHT // 2)
CLOCK = pygame.time.Clock()
OBSTACLES_LIMIT = 4
OBSTACLES:List[Obstacles] = []


def create_obstacles():
    i = 1
    while i <= OBSTACLES_LIMIT:
        radius = random.randint(50, 150)
        x = random.randint(0+radius, WIDTH-radius)
        y = random.randint(0+radius, HEIGHT-radius)
        if not pygame.Vector2(x, y).distance_to(PLAYER.position) <= radius + PLAYER.radius:
            OBSTACLES.append(Obstacles(WORLD, x, y, radius))
            i += 1


def initialize_world():
    pygame.init()
    pygame.display.set_caption('Zombie mod')
    create_obstacles()
    WORLD.fill(BACKGROUND)
    pygame.display.flip()
    PLAYER.draw()
    for obstacle in OBSTACLES:
        obstacle.draw()


def redraw():
    WORLD.fill(BACKGROUND)
    PLAYER.draw()
    for obstacle in OBSTACLES:
        obstacle.draw()
    pygame.display.update()


def get_input(player):
    keys = pygame.key.get_pressed()
    key_directions = {
        pygame.K_LEFT: (-player.speed, 0),
        pygame.K_RIGHT: (player.speed, 0),
        pygame.K_UP: (0, -player.speed),
        pygame.K_DOWN: (0, player.speed),
    }

    for key, (dx, dy) in key_directions.items():
        if keys[key] and not player.check_collide_with_obstacles(OBSTACLES, dx, dy) and player.is_not_out_of_border(
                WIDTH, HEIGHT, dx, dy):
            if dx == -player.speed:
                player.move('LEFT')
            elif dx == player.speed:
                player.move('RIGHT')
            elif dy == -player.speed:
                player.move('UP')
            elif dy == player.speed:
                player.move('DOWN')


if __name__ == '__main__':
    initialize_world()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        get_input(PLAYER)
        redraw()
    CLOCK.tick(60)
