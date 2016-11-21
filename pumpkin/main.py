import sys
import pygame
from pygame import *
from pygame.sprite import Group, OrderedUpdates
from libs import level_map
from controller import Controller
import units
import gamestats
import paths

class MyGroup(Group):
    def __init__(self, name, *sprites):
        super().__init__(*sprites)
        self.name = name

bg_layer = MyGroup('bg')
dors = MyGroup('dors')
walls = MyGroup('walls')


def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("pumpkin_maze")
    # Запуск основного цикла игры.
    stats = gamestats.GameStat()
    maps = ('maps/map1.json', 'maps/map2.json')
    levels = level_map.Levels(maps, screen, paths.resources, bg_layer, walls, dors)
    up = down = left = right = running = False
    player = units.Player(stats, screen, 1, 1, 27, 27)
    timer = pygame.time.Clock()
    while True:
        timer.tick(120)
        # Отслеживание событий клавиатуры и мыши.
        controll = Controller(player)
        # Отображение последнего прорисованного экрана.

        screen.fill((0,0,0))
        levels[stats.level].draw(screen)
        player.blitme()
        player.update(levels[stats.level])
        pygame.display.flip()


run_game()
