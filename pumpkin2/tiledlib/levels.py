# coding=utf-8

"""
модуль создаёт и выводит на экран карту

"""
import os

import pygame
from pumpkin2.exemples.test_level import msprites as spr
from pumpkin2.tiledlib.map_loader import TiledMap, SubSprites


class Levels:
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
        self.validate_maps = []
        self.levels = []

        self.__create_levels()

    def __create_levels(self):
        # создаём список валидных карт TiledMap
        self.validate_maps.extend(self.__get_validate_tiled_map())
        if self.validate_maps:
            for tiled_map in self.validate_maps:
                level = Level(self.screen, self.root, tiled_map)
                self.add_level(level)

    def add_level(self, level):
        self.levels.append(level)



    def _get_level_path(self, level_name):
        return os.path.join(self.root, self.levels_dir, level_name,
                            Levels.level_map_name)

    def __get_validate_tiled_map(self):

        """
        список объектов TiledMap
        :return: list < TiledMap
        """
        validate_maps = []
        not_maps_paths = []
        for name_level in self._included_levels:
            full_path = self._get_level_path(name_level)
            if os.path.isfile(full_path):
                map_dct = TiledMap.load_map(full_path)
                tiled_map = TiledMap(map_dct, self.root)
                validate_maps.append(tiled_map)
            else:
                not_maps_paths.append(full_path)
        if not_maps_paths:
            print(''' этих карт не существует - {}'''.format(not_maps_paths))
        return validate_maps

    def draw(self, level):
        self.levels[level].draw(self.screen)

    # def __str__(self):
    #     return 'доступные уровни - {}'.format(
    #         list([x for x in self.validate_maps]))




class Level(pygame.sprite.Group):
    def __init__(self, screen, root, tiled_map: TiledMap):
        """

        :param screen: ссылка на поверхность главного окна
        :param root: путь к корневому каталогу игры
        :param tiled_map_path: карта json
        """
        super().__init__()
        self._tiled_map = tiled_map
        self.root = root
        self.screen = screen
        self.sub_sprites = self.tiled_map.sub_sprites(SubSprites)
        self.__create_level()

    @property
    def tiled_map(self):
        return self._tiled_map

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
