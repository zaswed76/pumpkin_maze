# coding=utf-8

"""
модуль создаёт и выводит на экран карту

"""
import os

import pygame
from pumpkin2.exemples.test_level import msprites as spr
from pumpkin2.tiledlib.map_loader import TiledMap, SubSprites


class Levels(list):
    level_map_name = 'map.json'
    def __init__(self, screen: pygame.Surface, root: str,
                 included_levels: list, levels_dir: str):

        """

        :param screen:
        :param root:
        :param init_levels: seq < str имена каталогов - уровней
        :param levels_dir: полный путь к каталогу с картами
        см. док к пакету maps
        """
        super().__init__()
        self.root = root
        self.screen = screen
        self.levels_dir = levels_dir
        self._included_levels = included_levels

    def _get_level_path(self, level_name):
        return os.path.join(self.root, self.levels_dir, level_name, Levels.level_map_name)


    @property
    def included_levels(self):
        validate_paths = []
        for name_level in self._included_levels:
            full_path = self._get_level_path(name_level)
            if os.path.isfile(full_path):
                map_dct = TiledMap.load_map(full_path)
                tiled_map = TiledMap(map_dct, self.root)
                validate_paths.append((tiled_map, name_level))
        return validate_paths

    def __str__(self):
        return 'доступные уровни - {}'.format(
            list([x[1] for x in self.included_levels]))


class Level(pygame.sprite.Group):
    def __init__(self, screen, root, tiled_map_path):
        """

        :param screen: ссылка на поверхность главного окна
        :param root: путь к корневому каталогу игры
        :param tiled_map_path: карта json
        """
        super().__init__()
        self.tiled_map_path = tiled_map_path
        self.root = root
        self.screen = screen
        map_dct = TiledMap.load_map(self.tiled_map_path)
        self.tiled_map = TiledMap(map_dct, self.root)
        self.sub_sprites = self.tiled_map.sub_sprites(SubSprites)
        self.__create_level()

    def __create_level(self):
        layers = self.tiled_map.layers
        for layer in layers:
            if layer['type'] == 'tilelayer':  # tiles
                self.__create_tilelayer(layer)
            elif layer['type'] == 'objectgroup':  # figure
                self.__create_objectgroup(layer)
            elif layer['type'] == 'imagelayer':  # image (bg)
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
        n_y = count // w_count
        x = width * int(count - (n_y * w_count))
        y = height * n_y
        return x, y
