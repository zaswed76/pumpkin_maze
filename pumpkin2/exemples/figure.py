

import sys
import pygame
from pumpkin2 import paths
from pumpkin2.tiledlib import tiled

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    level_pth = paths.get_map('level_1')
    level = tiled.Tiled.load_map(level_pth)
    poly_line = level['layers'][0]['objects'][0]['polyline']

    print(poly_line)
    ln = [(d['x'], d['y']) for d in poly_line]
    print(ln)


    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        screen.fill(pygame.Color('grey'))
        pygame.draw.lines(screen, 0xffffff, False, ln, 1)
        pygame.display.flip()

run_game()