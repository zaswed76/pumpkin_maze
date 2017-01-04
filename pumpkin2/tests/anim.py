__author__ = 'lyuda'

# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.sprite import Group
from pumpkin2.tiledlib.map_loader import Sub, TiledMap
from pumpkin2.tiledlib import map_loader

from pumpkin2.gamelib.sprites import GameObject
from pumpkin2 import paths


def create_sprites(screen, sprites, group, x, y):
    y = y
    x = x
    step = 32
    for sp in sprites:
        img = GameObject(group, screen, sp, x, y)
        x += step
        group.add(img)


def tiled_sprites():
    path = paths.get_map('level_1')
    mp = TiledMap.load_map(path)
    tiled_map = TiledMap(mp, paths.exsets)
    sprites = tiled_map.sub_sprites
    return sprites


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.group = Group()

    def run(self):
        while True:
            # Отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(pygame.Color('#D8D8D8'))
            self.group.draw(self.screen)
            pygame.display.flip()

    def create_sprites(self, sprites, x, y):
        y = y
        x = x
        step = 32

        if isinstance(sprites, (list, map_loader.ListMap)):
            for sp in sprites:
                img = GameObject(self.group, self.screen, sp, x, y)
                x += step
                self.group.add(img)
        elif isinstance(sprites, pygame.Surface):
            img = GameObject(self.group, self.screen, sprites, x, y)
            self.group.add(img)

if __name__ == '__main__':
    def test_get_sprites():
        player = Sub(paths.get_exsets('set_4x1_transparent.png'), 32,
                      32).get_sprites()
        var = player[0]
        game.create_sprites(var, 10, 10)

    def test_get_back_sprites():
        player = Sub(paths.get_exsets('set_4x1_transparent.png'), 32,
                      32).get_sprites_back()
        game.create_sprites(player, 10, 50)

    def test_tilesets_sprites():
        tiled_map = TiledMap(TiledMap.load_map("map.json"), './')
        sprites = tiled_map.sub_sprites[1]
        game.create_sprites(sprites, 10, 50)

    def test_get_sprite(gid):
        player = Sub(paths.get_exsets('set_4x1_transparent.png'), 32,
                      32).get_sprite(gid)
        game.create_sprites(player, 10, 10)

    game = Game()

    # test_get_sprites()
    # test_get_sprite(0)
    # test_get_back_sprites()
    # test_tilesets_sprites()
    game.run()