from collections import OrderedDict
import pygame
import gamestats
import paths
from controller import Controller
from libs import level_map
from libs import units
from config import Config

cfg = Config()


# bg_layer = units.MyGroup('bg')
blocks = OrderedDict()
blocks['doors'] = units.MyGroup('doors')
blocks['wooden_walls'] = units.MyGroup('walls')
blocks['stone_walls'] = units.MyGroup('walls')


def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((768, 640))
    pygame.display.set_caption("pumpkin_maze")
    # Запуск основного цикла игры.
    stats = gamestats.GameStat()
    dir = level_map.get_map_files(paths.maps)
    maps = level_map.get_map_files(paths.maps)

    levels = level_map.Levels(maps, screen, paths.resources, **blocks)
    player = units.Player(stats, screen, cfg.speedx, cfg.speedy, 27, 27)
    timer = pygame.time.Clock()
    while True:
        timer.tick(120)
        # Отслеживание событий клавиатуры и мыши.
        controller = Controller(player)
        # Отображение последнего прорисованного экрана.

        screen.fill((0,0,0))
        levels[stats.level].draw(screen)
        player.blitme()
        player.update(levels[stats.level])
        pygame.display.flip()


run_game()
