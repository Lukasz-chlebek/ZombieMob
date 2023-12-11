import pygame
import random
import globals
from Obstacles.obstacles import Obstacles
from Enemy.enemy import Enemy

def create_obstacles():
    i = 1
    while i <= globals.OBSTACLES_LIMIT:
        radius = random.randint(50, 100)
        x = random.randint(0+radius, globals.WIDTH-radius)
        y = random.randint(0+radius, globals.HEIGHT-radius)
        if not pygame.Vector2(x, y).distance_to(globals.PLAYER.position) <= radius + globals.PLAYER.radius:
            globals.OBSTACLES.append(Obstacles(globals.WORLD, x, y, radius))
            i += 1

def create_enemy():
    global x_pos, y_pos
    i = 1
    const_dist = 500
    while i <= globals.ENEMIES_LIMIT:
        direction = random.randrange(4)
        if direction == 0:
            x_pos = random.randrange(0, globals.WIDTH)
            y_pos = -const_dist
        elif direction == 1:
            x_pos = globals.WIDTH + const_dist
            y_pos = random.randrange(0, globals.HEIGHT)
        elif direction == 2:
            x_pos = random.randrange(0, globals.WIDTH)
            y_pos = globals.HEIGHT + const_dist
        elif direction == 3:
            x_pos = -const_dist
            y_pos = random.randrange(0, globals.HEIGHT)
        globals.ENEMIES.append(Enemy(globals.WORLD, x_pos, y_pos))
        i += 1


def initialize_world():
    pygame.init()
    pygame.display.set_caption('Zombie mod')
    create_obstacles()
    create_enemy()
    globals.WORLD.fill(globals.BACKGROUND)
    pygame.display.flip()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    globals.PLAYER.draw(mouse_x,mouse_y)
    for obstacle in globals.OBSTACLES:
        obstacle.draw()


def redraw():
    globals.WORLD.fill(globals.BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    globals.PLAYER.draw(mouse_x, mouse_y)
    for obstacle in globals.OBSTACLES:
        obstacle.draw()
    for bullet in globals.BULLETS:
        any_hits, hit_enemy = bullet.check_collide_with_enemy(globals.ENEMIES)
        if bullet.check_collide_with_obstacles(globals.OBSTACLES) or bullet.is_out_of_border(globals.WIDTH,globals.HEIGHT) or any_hits:
            globals.BULLETS.remove(bullet)
            if any_hits:
                globals.ENEMIES.pop(hit_enemy)
        bullet.draw(globals.CLOCK.get_time() / 1000.0)

    for enemy in globals.ENEMIES:
        enemy.draw()
    for liness in globals.lines:
        liness.draw()

    globals.clear_lines()
    pygame.display.update()

def get_mouse(player):
    mouse_position = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed(3)[0]:
        globals.BULLETS.append(player.shoot(mouse_position))


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
    for enemy in globals.ENEMIES:
        enemy.update(deltaTime)
    globals.PLAYER.update(deltaTime)

if __name__ == '__main__':
    initialize_world()
    running = True
    while running:
        deltaTime = globals.CLOCK.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse(globals.PLAYER)
        get_input(globals.PLAYER, deltaTime)
        update(deltaTime)
        redraw()
        globals.CLOCK.tick(60)
