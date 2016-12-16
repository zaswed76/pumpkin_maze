import os
from collections import OrderedDict
import pygame
import pumpkin
import gamestats
import paths
from controller import Controller

from libs import game_groups, player, mapcreator
from config import Config

cfg = Config()
print('{} = {}'.format('ver', pumpkin.__version__))


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
    level_creator = mapcreator.LevelCreator(screen, paths.maps, paths.tilesets, paths.resources, cfg)


    level_creator.create_level(stats.level)

    inventory = game_groups.Inventory()
    player_unit = player.Player(stats, screen, 2, 2, cfg, inventory=inventory)
    timer = pygame.time.Clock()
    # Запуск основного цикла игры.

    while True:

        # Отслеживание событий клавиатуры и мыши.
        controller = Controller(stats, level_creator=level_creator, player=player_unit)
        # Отображение последнего прорисованного экрана.

        # print(player_unit.breaks)
        level_creator.draw()
        player_unit.blitme()
        player_unit.update(level_creator.level.all_layers.get_groups(), level=level_creator)
        pygame.display.flip()
        timer.tick(120)



run_game()
