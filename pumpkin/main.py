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
    screen = pygame.display.set_mode((320, 320))
    pygame.display.set_caption("pumpkin_maze")
    # Запуск основного цикла игры.
    stats = gamestats.GameStat()
    # dir = level_map.get_map_files(paths.maps)
    # maps = level_map.get_map_files(paths.maps)
    json_map = os.path.join(paths.maps, 'map1.json')
    levels = mapcreator.MapCreator(json_map, paths.tilesets, screen)
    levels.create_map()
    # player = units.Player(stats, screen, cfg.speedx, cfg.speedy, 27, 27)
    timer = pygame.time.Clock()
    while True:
        timer.tick(120)
        # Отслеживание событий клавиатуры и мыши.
        controller = Controller()
        # Отображение последнего прорисованного экрана.

        screen.fill((0,0,0))
        levels.draw_map()
        # player.blitme()
        # player.update(levels[stats.level])
        pygame.display.flip()


run_game()
