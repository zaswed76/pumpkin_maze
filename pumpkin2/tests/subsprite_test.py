# -*- coding: utf-8 -*-
import sys

import pygame
from pygame.sprite import Group
from pumpkin2 import paths
from pumpkin2.gamelib import sprites
from pumpkin2.tiledlib import map_loader as tl
from pumpkin2.tiledlib.map_loader import *
print(tl.__doc__)

def create_image(screen, image, pos):
    group = Group()
    return sprites.GameObject(group, screen, image, pos[0], pos[1])

def create_image_2(image):
    img = pygame.image.load(image).convert_alpha()
    return img

def run_game():
    tmap = tl.TiledMap.load_map(paths.get_map('level_1'))
    tiled = tl.TiledMap(tmap, paths.exsets)

    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode(tiled.size)
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    sprite = tiled.sub_sprites[7]
    # print(tiled.sub_sprites)
    img = create_image(screen, sprite, (1, 1))
    # img = create_image_2(paths.get_exsets("100x50x4.png"))



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