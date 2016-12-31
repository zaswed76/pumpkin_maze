# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.sprite import Group
from pumpkin2.gamelib import sprites
from pumpkin2.tiledlib import subsprite
from pumpkin2 import paths
from pumpkin2 import paths
from pumpkin2.tiledlib import subsprite, tiled
from pumpkin2.tiledlib import tiled as tl
from pumpkin2.tiledlib import tiled_to_spites

def sprites_img(level, set_dir):
    tmap = tl.Tiled.load_map(level)
    tiled = tl.Tiled(tmap, set_dir)
    return tiled.sub_sprites

def run_game():
    tmap = tl.Tiled.load_map(paths.get_map('level_1'))
    tiled = tl.Tiled(tmap, paths._exsets)
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode(tiled.size)
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.

    group = Group()
    image = tiled.sub_sprites[14]
    print(image)
    img = sprites.GameObject(group, screen, image, 32, 32)

    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        screen.fill(pygame.Color('#D8D8D8'))
        img.draw(screen)
        pygame.display.flip()

run_game()