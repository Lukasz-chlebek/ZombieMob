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
    while len(globals.ENEMIES) <= globals.ENEMIES_LIMIT and i < 5:
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

def reinitialize_globals():
    globals.SCORE = 0
    globals.OBSTACLES = []
    globals.ENEMIES = []
    globals.PLAYER.position = pygame.Vector2(globals.WIDTH / 2, globals.HEIGHT / 2)
    globals.PLAYER.is_alive = True

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
                globals.SCORE += 10
                globals.ENEMIES.pop(hit_enemy)
        bullet.draw(globals.CLOCK.get_time() / 1000.0)

    for enemy in globals.ENEMIES:
        enemy.draw()
    
    if globals.debug_draw:
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
    if random.random() < 0.01:
        create_enemy()
    for enemy in globals.ENEMIES:
        enemy.update(deltaTime)
    globals.PLAYER.update(deltaTime)

def end_screen():
    if globals.SCORE > globals.BEST_SCORE:
        globals.BEST_SCORE = globals.SCORE
    globals.WORLD.fill(globals.BACKGROUND)
    font = pygame.font.Font('Merchandise.ttf', 32)
    text = font.render('Best Score: ' + str(globals.BEST_SCORE), True, globals.FOREGROUND,
                       globals.BACKGROUND)
    text2 = font.render('Your Score: ' + str(globals.SCORE) + ' Press "R" to restart or "Q" to close game', True, globals.FOREGROUND, globals.BACKGROUND)
    textRect = text.get_rect()
    textRect.center = (globals.WIDTH // 2, globals.HEIGHT // 2)
    textRect2 = text2.get_rect()
    textRect2.center = (globals.WIDTH // 2, globals.HEIGHT // 2 - 100)
    globals.WORLD.blit(text, textRect)
    globals.WORLD.blit(text2, textRect2)
    pygame.display.update()

def main():
    reinitialize_globals()
    initialize_world()
    is_end_screen = False
    running = True
    while running:
        deltaTime = globals.CLOCK.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse(globals.PLAYER)
        if not globals.PLAYER.is_alive:
            is_end_screen = True
            running = False
        get_input(globals.PLAYER, deltaTime)
        update(deltaTime)
        redraw()
        globals.CLOCK.tick(60)
    while is_end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_end_screen = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()
        if keys[pygame.K_q]:
            is_end_screen = False
        end_screen()


if __name__ == '__main__':
    main()


