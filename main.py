import pygame
import random
from globals import *


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
        if bullet.check_collide_with_obstacles(OBSTACLES) or bullet.is_out_of_border(WIDTH,HEIGHT) or any_hits:
            BULLETS.remove(bullet)
            if any_hits:
                ENEMIES.pop(hit_enemy)
        bullet.draw(CLOCK.get_time() / 1000.0)

    for enemy in ENEMIES:
        enemy.draw()
    pygame.display.update()

def get_mouse(player):
    mouse_position = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed(3)[0]:
        BULLETS.append(player.shoot(mouse_position))


def get_input(player, deltaTime:float):
    keys = pygame.key.get_pressed()
    key_directions = {
        pygame.K_LEFT: (1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0,1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0),
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1)
    }

    direction = pygame.Vector2(0,0)
    for key, (dx, dy) in key_directions.items():
        if keys[key]:
            direction += pygame.Vector2(dx, dy)
    if direction.length_squared() > 0:
        direction.normalize_ip()
    player.set_direction(direction)

def update(deltaTime:float):
    for enemy in ENEMIES:
        enemy.update(deltaTime)
    PLAYER.update(deltaTime)

if __name__ == '__main__':
    initialize_world()
    running = True
    while running:
        deltaTime = CLOCK.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse(PLAYER)
        get_input(PLAYER, deltaTime)
        update(deltaTime)
        redraw()
        CLOCK.tick(60)
