import pygame


def initialize_window_and_run():
    background_colour = (0, 0, 0)
    (width, height) = (1280, 960)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Zombie mod')
    screen.fill(background_colour)
    pygame.display.flip()


if __name__ == '__main__':
    initialize_window_and_run()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
