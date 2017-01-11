# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.sprite import Group
from pumpkin2.exemples.test_level import msprites as spr
from pumpkin2.tiledlib.map_loader import TiledMap, SubSprites
from pumpkin2 import paths


def lvss():
    lvs = list()
    lvs.append(spr.ABCSprite(spr.Rect, size=(50, 50), pos=(0, 0), color='green'))
    lvs.append(spr.ABCSprite(spr.Rect, size=(50, 50), pos=(110, 110), color='red'))
    return lvs
class Level(pygame.sprite.Group):
    def __init__(self, screen, root):
        super().__init__()
        self.root = root
        self.screen = screen
        self.__create_level()
        # sprite = spr.ABCSprite(spr.Image, image=self.image)

    def __create_level(self):
        path = paths.get_map('level_1')
        # path = r'D:\save\serg\projects\pumpkin_maze\pumpkin2\map.json'
        map_dct = TiledMap.load_map(path, self.root)
        tiled_map = TiledMap(map_dct, paths.exsets)
        self.sub_sprites = tiled_map.sub_sprites(SubSprites)
        layers = tiled_map.layers

        # print(sub_image)
        for layer in layers:
            if layer['type'] == 'tilelayer': # tiles
                self.__create_tilelayer(layer)
            elif layer['type'] == 'objectgroup': # figure
                self.__create_objectgroup(layer)
            elif layer['type'] == 'imagelayer': # image (bg)
                self.__create_image(layer)

    def __create_tilelayer(self, layer):
        if layer['visible']:
            for count, gid in enumerate(layer['data'], start=0):
                if gid:
                    self.__create_tile(gid, count, layer['width'])

    def __create_objectgroup(self, layer):
        if layer['visible']:
            print('create_objectgroup')

    def __create_image(self, layer):
        if layer['visible']:
            print('create_image')

    def __create_tile(self, gid, count, layer_width):
        sprite = spr.ABCSprite(spr.Image,
                               image=self.sub_sprites[gid])
        pos = self.__get_sprite_pos(count, sprite.rect.width,
                                    sprite.rect.height, layer_width)
        sprite.set_pos(pos)
        self.add(sprite)


    def __get_sprite_pos(self, count, width, height, w_count):
        """
        вычисляет координату верхнего левого угла спрайта
        :param n: порядковый номер от 0
        :param width: width sprite
        :param height: height sprite
        :param w_count: спрайтов по горизонтали
        :return: tuple < int, int
        """
        # print('----------')
        # print(width)
        # print(height)
        # print(w_count)
        # print('------------')
        n_y = count // w_count
        x = width * int(count - (n_y * w_count))
        y = height * n_y
        return x, y
