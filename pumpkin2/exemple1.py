# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.sprite import Group
from pumpkin2.gamelib import sprites
from pumpkin2.tiledlib import subsprite
from pumpkin2 import paths



def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    sub = subsprite.SubSprite(paths.get_exsets('100x50x4.png'), 100, 50)
    sprites_img = sub.get_sprites()
    group = Group()
    image = sprites_img[3]
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