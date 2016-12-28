import os
from collections import OrderedDict
import pygame
import gamestats
import paths
from controller import Controller

from libs import game_groups, player, mapcreator
from config import Config

cfg = Config()


def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    # json_map = os.path.join(paths.maps, '5.json')
    screen = pygame.display.set_mode((cfg.width, cfg.height))
    # level = mapcreator.MapCreator(screen, json_map, paths.tilesets,
    #                                paths.resources)

    # level.set_screen(screen)
    pygame.display.set_caption("pumpkin_maze")

    stats = gamestats.GameStat(cfg)
    # level.create_map()

    #---------- Levels ----------------------------------------------
    all_levels = mapcreator.Levels(screen, paths.maps, paths.tilesets_dir, paths.resources, cfg)


    all_levels.create_levels(stats.level)

    inventory = game_groups.Inventory()
    player_unit = player.Player(stats, screen, 2, 2, cfg, inventory=inventory)
    timer = pygame.time.Clock()
    # Запуск основного цикла игры.

    while True:

        # Отслеживание событий клавиатуры и мыши.
        controller = Controller(stats, level=all_levels, player=player_unit)
        # Отображение последнего прорисованного экрана.

        # print(player_unit.breaks)
        all_levels.draw(stats.level)
        player_unit.blitme()
        player_unit.update(all_levels[0].all_layers.get_groups(), level=all_levels)
        pygame.display.flip()
        timer.tick(120)



run_game()
