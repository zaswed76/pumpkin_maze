import os
import sys

import paths

import pygame
from pygame.sprite import Group

from pygame.sprite import Sprite

from libs import tiledmap


class Platform(Sprite):
    def __init__(self, screen, image, x, y, size: tuple):
        # todo Ограничение перемещений
        super().__init__()
        self.image = image
        self.screen = screen
        # Загрузка изображения корабля и получение прямоугольника.
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, *size)



    def blitme(self):
        self.screen.blit(self.image, self.rect)

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    pth_map = os.path.join(paths.maps, 'map1.json')
    tiled = tiledmap.TiledParser(pth_map, paths.tilesets)
    sprites = tiled.get_subsprites(tiled.get_id_tiles())
    player = Platform(screen, sprites[15], 0, 0, (32, 32))
    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        screen.fill(pygame.Color('grey'))
        player.blitme()

        pygame.display.flip()

run_game()
