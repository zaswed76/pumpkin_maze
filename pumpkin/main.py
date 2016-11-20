import sys
import pygame
from pygame.sprite import Group, OrderedUpdates
from libs import level_map
import paths

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("pumpkin_maze")
    # Запуск основного цикла игры.
    all_group = pygame.sprite.OrderedUpdates()
    levels = []
    for i in range(100):
        level_1 = level_map.LevelMap('maps/map1.json', screen, all_group, imgset_dir=paths.resources)
        walls = Group()
        level_1.create_map(walls)
        levels.append(level_1)
    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        levels[0].draw_layers()
        pygame.display.flip()

run_game()