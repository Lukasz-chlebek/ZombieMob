import pygame
import random
from typing import List

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
OBSTACLES_LIMIT = 4
OBSTACLES:List[Obstacles] = []
BULLETS:List[Bullet] = []

ENEMIES:List[Enemy] = [Enemy(WORLD, WIDTH//2, HEIGHT//2)]

def create_obstacles():
    i = 1
    while i <= OBSTACLES_LIMIT:
        radius = random.randint(50, 100)
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
    for bullet in BULLETS:
        any_hits, hit_enemy = bullet.check_collide_with_enemy(ENEMIES)
        if bullet.check_collide_with_obstacles(OBSTACLES) or bullet.is__out_of_border(WIDTH,HEIGHT) or any_hits:
            BULLETS.remove(bullet)
            if any_hits:
                ENEMIES.pop(hit_enemy)
        bullet.draw()

    for enemy in ENEMIES:
        enemy.draw()
    pygame.display.update()


def get_mouse(player):
    mouse_position = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed(3)[0]:
        BULLETS.append(player.shoot(mouse_position))


def get_input(player):
    keys = pygame.key.get_pressed()
    key_directions = {
        pygame.K_LEFT: (-player.speed, 0),
        pygame.K_RIGHT: (player.speed, 0),
        pygame.K_UP: (0, -player.speed),
        pygame.K_DOWN: (0, player.speed),
        pygame.K_a: (-player.speed, 0),
        pygame.K_d: (player.speed, 0),
        pygame.K_w: (0, -player.speed),
        pygame.K_s: (0, player.speed)
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

def update(deltaTime:float):
    for enemy in ENEMIES:
        enemy.update(deltaTime)


if __name__ == '__main__':
    initialize_world()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse(PLAYER)
        get_input(PLAYER)
        update(CLOCK.get_time() / 1000.0)
        redraw()
        CLOCK.tick(60)
