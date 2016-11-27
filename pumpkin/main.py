import os
from collections import OrderedDict
import pygame
import gamestats
import paths
from controller import Controller
from libs import mapcreator
from libs import units
from config import Config

cfg = Config()


def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    # json_map = os.path.join(paths.maps, '5.json')
    screen = pygame.display.set_mode((320, 320))
    # level = mapcreator.MapCreator(screen, json_map, paths.tilesets,
    #                                paths.resources)

    # level.set_screen(screen)
    pygame.display.set_caption("pumpkin_maze")

    stats = gamestats.GameStat()
    # level.create_map()

    #---------- Levels ----------------------------------------------
    all_levels = mapcreator.Levels(screen, paths.maps, paths.tilesets, paths.resources, cfg)

    all_levels.create_levels()

    timer = pygame.time.Clock()
    # Запуск основного цикла игры.
    while True:

        # Отслеживание событий клавиатуры и мыши.
        controller = Controller(stats, level=all_levels[stats.level])
        # Отображение последнего прорисованного экрана.


        all_levels.draw(stats.level)

        pygame.display.flip()
        timer.tick(120)



run_game()
