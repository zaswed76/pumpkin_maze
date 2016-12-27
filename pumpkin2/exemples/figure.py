

import sys
import pygame
from pumpkin2 import paths
from pumpkin2.tiledlib import abctiled, printer


def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((320, 320))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    level_pth = paths.get_map('level_1')
    level = abctiled.Tiled.load_map(level_pth)
    layer = level['layers'][0]
    fobject = layer['objects'][0]
    fobjects = layer['objects']
    color = layer['color']
    poly_line = layer['objects'][0]['polyline']
    offset_x = fobject['x']
    offset_y = fobject['y']
    printer.print_list(fobjects)
    ln = [(d['x'] + offset_x, d['y'] + offset_y) for d in poly_line]
    # print(ln)


    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        screen.fill(pygame.Color('grey'))
        line = pygame.draw.aalines(screen, pygame.Color(color), 1, ln)
        # line = pygame.draw.lines(screen, pygame.Color(color), False, ln, 1)
        # print(line)
        pygame.display.flip()

run_game()