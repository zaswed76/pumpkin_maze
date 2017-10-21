# coding=utf-8

"""
модуль предоставляет классы для работы с картой сгенерирваной
програмой Tiled Map Editor. карта представляет собой
словарь.
class SubSprites создаёт и возвращает последовательность спрайтов - 'Surface'
class TiledMap - обёртка над словарём предсставляющем карту Tiled Map Editor

"""
import json
import os
from abc import ABCMeta, abstractmethod

import pygame

from tiledlib.tilesets import *

__all__ = ["TiledMap", "TiledSubSprites"]


class MapErrors(Exception):
    pass


class ListMap:
    '''
    класс контейнер для спрайтов с индексацией с 1

    '''

    def __init__(self):
        """
        ! индксация начинается с 1
        обращение к 0 или отрицательному индексу вызовет исключение
        выход за пределы списка так же вызовет исключение
        """
        self._sprites = []
        self.__value = 0

    def append(self, item):
        self._sprites.append(item)

    def __iter__(self):  # Возвращает итератор в iter()
        return self

    def __next__(self):
        if self.__value == len(self._sprites):
            raise StopIteration

        z = self._sprites[self.__value]
        self.__value += 1
        return z

    def __getitem__(self, key):
        """
        """
        if isinstance(key, slice):
            # noinspection PyTypeChecker
            assert key.start > 0, "'Index sprites list starts with 1'"
            return self._sprites[key.start - 1: key.stop]
        else:
            assert key > 0, 'Index sprites list starts with 1'
            print(key, 555)
            assert key <= len(self._sprites), \
                '''Length is the list of sprites - {}'''.format(
                    len(self._sprites))
            return self._sprites[key - 1]

    def __add__(self, other):
        if isinstance(other, TiledSubSprites):
            self._sprites.extend(other)
            return self._sprites
        else:
            raise TypeError(
                'слагаемое должно быть объктом класса SubSprites')

    def __len__(self):
        return len(self._sprites)

    def __repr__(self):
        return str(self._sprites)


class ABCSubImages(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self.image = kwargs.get('image')
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')

    @abstractmethod
    def get_sprites(self):
        """
        :return последовательность  объктов изображений
        """
        pass

    @abstractmethod
    def get_image_sprite(self, img):
        """
        :return объект изображения
        """
        pass


class SubSprites(ABCSubImages):
    """ класс предоставляет методы для 'вырезания и зоздания
     спрайтов из изображения ' """

    def __init__(self, **kwargs):
        """

        :param image: str путь к изображению
        :param width: ширина спрайта
        :param height: высота спрайта
        """

        super().__init__(**kwargs)
        self.image = kwargs.get('image')
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        if self.image is not None:
            self.sprite = pygame.image.load(self.image).convert_alpha()
            self.sprite_rect = self.sprite.get_rect()
            # спрайтов по горизонтали
            self.w_count = self.sprite_rect.width // self.width
            # спрайтов по вертикали
            self.h_count = self.sprite_rect.height // self.height

    def get_coord(self, n, width, height, w_count):
        """
        вычисляет координату верхнего левого угла спрайта
        :param n: порядковый номер от 0
        :param width:
        :param height:
        :param w_count: спрайтов по горизонтали
        :return:
        """
        n_y = n // w_count
        x = width * int(n - (n_y * w_count))
        y = height * n_y
        return x, y

    def get_sprite(self, n):
        """

        :param n: порядковый номер
        :return: Surface
        """
        x, y = self.get_coord(n, self.width, self.height,
                              self.w_count)
        return self.sprite.subsurface((x, y, self.width, self.height))

    def get_sprites(self, s: int = 0, count: int = None) -> list:
        """

        :param s: начало вырезания
        :param count:  колличество вырезаных
        :return: list < pygame.Surface последовательность спрайтов
        отсчёт начинается с 0
        """
        lst = list()
        if count is None:
            f = self.w_count * self.h_count
        else:
            f = s + count + 1
        for x in range(s, f):
            lst.append(self.get_sprite(x))
        return lst

    # noinspection PyMethodOverriding
    def get_image_sprite(self, img):
        return pygame.image.load(img).convert_alpha()

    def get_sprites_back(self):
        """
        создаёт спрайты из изображения (для анимации)
        с вовратом
        [0, 1, 2, 3, 2, 1]
        :return: lst < Surface
        """
        n = int(self.w_count)
        lst = list(range(n))
        res = [self.get_sprite(x) for x in lst]
        back = res[::-1]
        res.extend(back[1:len(back) - 1])
        return res

    @staticmethod
    def get_sprite_time(s, t):
        return [(x, t) for x in s]

    def __repr__(self):
        return '''
        class - {}
        tileset - {}
        self.w_count - {}
        self.h_count - {}
        size - ({}, {})

        '''.format(self.__class__, self.image, self.w_count,
                   self.h_count, self.width, self.height)


class TiledSubSprites(ListMap):
    """
    класс является контейнером для спрайтов созданных на основании данных
    объкта TileSets. Может создавать спрайты на основании тайлсетов
    и коллекций изображений
    """

    def __init__(self, images_fabric, tilesets):
        """ индексация начинается с 1
            ! читать doc к ListMap
            получает один параметр tilesets объект класса TileSets
            отображение параметра 'tilesets' карты
            SubSprites(tilesets: TileSets)
            :param images_fabric наследник класса ABCSubImages
            """
        super().__init__()
        self.sprites_fabric = images_fabric
        if not isinstance(images_fabric, ABCMeta):
            raise TypeError('''images_fabric лолжен быть
            наследником класса ABCSubImages''')

        self.__value = 0
        self.tilesets = tilesets
        assert isinstance(self.tilesets, TileSets), \
            "параметр tilesets должен быть объектом класса - {}".format(
                TileSets.__class__.__name__
            )
        self._create_sets_sprites()

    def _create_sets_sprites(self):
        """
        на основе тайлсетов из сгенерированой карты
        """
        for tset in self.tilesets:
            # если тайлсет (вырезает)
            if isinstance(tset, TileSet):
                image = tset.image
                w = tset.tilewidth
                h = tset.tileheight
                self.sub = self.sprites_fabric(image=image, width=w, height=h)
                self._sprites.extend(self.sub.get_sprites())
            # коллекция изображений
            elif isinstance(tset, ImageCollection):
                for img in tset.images:
                    sub = self.sprites_fabric()
                    self._sprites.append(
                        sub.get_image_sprite(img))


class TiledMap:
    """
    класс представляет карту сгенерированую Tiled Map Editor,
    где атрибуты соответствуют ключам словаря сгенерированой карты
    """
    default_orientation = 'orthogonal'

    def __init__(self, map_dict: dict, root: str, **kwargs):
        """
         карта в виде словаря
        :param sets_dir: путь к каталогу с тайлсетами
        :param map_dict:
        :param kwargs:
        """
        self.root = root
        self.__map_dict = map_dict

        # region поля словаря карты

        self._tilesets = TileSets(map_dict.get("tilesets", []),
                                  root=self.root)
        self.layers = map_dict.get("layers")
        # Stores the next available ID for new objects.
        self.nextobjectid = map_dict.get("nextobjectid")
        self.orientation = map_dict.get("orientation")
        self.renderorder = map_dict.get("renderorder")
        self.tileheight = map_dict.get("tileheight")

        self.tilewidth = map_dict.get("tilewidth")
        self.tilewidth = map_dict.get("tilewidth")
        self.version = map_dict.get("version")
        self.width = map_dict.get("width")
        self.properties = map_dict.get("properties")
        self.backgroundcolor = map_dict.get("backgroundcolor")
        self.propertytypes = map_dict.get("propertytypes")
        self.height = map_dict.get("height")
        # endregion
        self.__check_card()

    def __check_card(self):
        """
        проверка карты на валидность
        """
        if not self.__map_dict:
            raise MapErrors('файл карты пуст')
        if self.orientation != TiledMap.default_orientation:
            raise MapErrors(
                'карта должна быть - {}'.format(TiledMap.default_orientation))
        if not isinstance(self.layers, list):
            raise MapErrors('слои должны быть в виде списка')
        if not isinstance(self.tilesets, TileSets):
            raise MapErrors('tilesets должны быть объектом класса TileSets')

    @property
    def tilesets(self) -> TileSets:
        """
        :return: объект класса TileSets
        """
        ts = self.__map_dict.get("tilesets", [])
        if not isinstance(ts, list): raise MapErrors('должен быть списком')
        return self._tilesets

    def sub_sprites(self, images_fabric: ABCSubImages) -> TiledSubSprites:
        """

        :param sprites_fabric: ссылка на класс наслдедующего
         абстрактный ABCSubImages
        :return:  TiledSubSprites < Surface
        """
        if not isinstance(images_fabric, ABCMeta):
            raise TypeError('''images_fabric лолжен быть
            наследником класса ABCSubImages''')
        return TiledSubSprites(images_fabric, self.tilesets)

    def __str__(self):
        return '''  class - {}
  layers - {}
  user_properties - {}
  width - {} tiles
  height - {} tiles
  count sets - {} sets
  '''.format(self.__class__.__name__,
             len(self.layers),
             self.properties,
             self.width,
             self.height,
             len(self.tilesets)
             )

    # @staticmethod
    # def get_path(rootw, tiled_set_image):
    #     suff = os.path.realpath(tiled_set_image).replace(rootw, "").strip()
    #     full = os.path.join(os.path.abspath(rootw), suff)
    #     return full

    @staticmethod
    def load_map(pth_map: str) -> dict:
        """

        :param pth_map: path to json map
        :return: map < dict
        """
        with open(pth_map, "r") as f:
            return json.load(f)

    @property
    def size(self):
        """
        размер карты
        :return: tuple < int, int
        """
        w = self.width * self.tilewidth
        h = self.height * self.tileheight
        return (w, h)


if __name__ == '__main__':
    # примеры исползьования
    # импорт модуля хранящего пути к ресурсам
    from pumpkin2 import paths

    # инициация pygame ! обязательно !
    pygame.init()

    # путь к json карте
    path_map = paths.get_map('level_1')
    # path_map = r'D:\save\serg\projects\pumpkin_maze\pumpkin2\map.json'
    # получить словарь из json карты
    maps = TiledMap.load_map(path_map)
    # каталог с изображениями тайлсетов
    sets_dir = paths.exsets
    tiled_map = TiledMap(maps, sets_dir)

    # print('-------------------')
    # print('''sub
    #  получить список объектов изображений вызовом
    #  метода sub_sprites и передачей ссылки на класс SubSprites :\n''')
    #
    # # создать объект TiledMap
    # tiled_map = TiledMap(maps, sets_dir)
    #
    # # получить subsprites можно после  иницализации дисплея screen
    # # создать поверхность дисплея
    screen = pygame.display.set_mode((10, 10))
    # # получить объекты изображений ИНДЕКСАЦИЯ НАЧИНАЕТСЯ С 1
    sub = tiled_map.sub_sprites(SubSprites)
    print(sub)
    # print("""------ ИНДКСАЦИЯ НАЧИНАЕТСЯ С 1 --------- :""")
    # print(sub[1])
    # print("""------sub[1] исключение --------- :""")
    # try:
    #     print(sub[0])
    # except AssertionError:
    #     print(" !!! вызвано исключение: индксация начинается с 1 ")
    #
    # print('############################################')
    # print(""" sub.get_sprites()
    # получить последовательность спрайтов непсредственно создав
    # объект класса SubSprites и вызова метода get_sprites
    # ! ИНАДКСАЦИЯ НАЧИНАЕТС С 0 ! """)
    # image = paths.get_exsets('set_4x1_transparent.png')
    # sub = SubSprites(image=image, width=32, height=32)
    # # ИНДКСАЦИЯ НАЧИНАЕТСЯ С 0
    # print(sub.get_sprites())
    # print("""------ sub.get_sprites()[0] ИНДКСАЦИЯ НАЧИНАЕТСЯ С 0 --------- :""")
    # print(sub.get_sprites()[0])
    # print("""------ sub.get_sprites_back() ИНДКСАЦИЯ НАЧИНАЕТСЯ С 0 --------- :""")
    # print(sub.get_sprites_back())
