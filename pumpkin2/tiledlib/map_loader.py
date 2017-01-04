"""
модуль предоставляет классы для работы с картой сгенерирваной
програмой Tiled Map Editor. карта представляет собой
словарь.
class SubSprites создаёт и возвращает последовательность спрайтов - 'Surface'
class TiledMap - обёртка над словарём предсставляющем карту Tiled Map Editor


"""
import os

import pygame

from pumpkin2.tiledlib import _abctiled

__all__ = ["TiledMap", "SubSprites"]


class _Sprites:
    """ класс создаёт последовательность спрайтов из изображения """


    def __init__(self):
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
            assert key.start > 0, "!!!"
            return self._sprites[key.start - 1: key.stop]
        else:
            assert key > 0, 'Index sprites list starts with 1'
            assert key <= len(self._sprites), \
                '''Length is the list of sprites - {}'''.format(
                    len(self._sprites))
            return self._sprites[key - 1]

    def __add__(self, other):
        if isinstance(other, SubSprites):
            self._sprites.extend(other)
            return self._sprites
        else:
            raise TypeError(
                'слагаемое должно быть объктом класса SubSprites')

    def __len__(self):
        return len(self._sprites)

    def __repr__(self):
        return str(self._sprites)


class Sub:
    """ класс предоставляет методы для 'вырезания и зоздания
     спрайтов из изображения ' """

    def __init__(self, image, width, height):
        """

        :param image: str путь к изображению
        :param width: ширина спрайта
        :param height: высота спрайта
        """
        # todo откуда список начинается в разных методах
        self.image = image
        self.height = height
        self.width = width
        self.sprite = pygame.image.load(image).convert_alpha()
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

    def get_sprites(self, s=0, count=None):
        """

        :param s: начало вырезания
        :param count:  колличество вырезаных
        :return: _Sprites < pygame.Surface последовательность спрайтов
        отсчёт начинается с 1
        """
        lst = _Sprites()
        if count is None:
            f = self.w_count * self.h_count
        else:
            f = s + count + 1
        for x in range(s, f):
            lst.append(self.get_sprite(x))
        return lst

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


class SubSprites(_Sprites):
    """ класс создаёт последовательность спрайтов из изображения """

    def __init__(self, **kwargs):
        """
            SubSprites(tilesets: _abctiled.TileSets)
            SubSprites(image: str, size: tuple(int, int))
            """
        super().__init__()
        # self._sprites = []
        self.__value = 0

        if 'tilesets' in kwargs:
            self.tilesets = kwargs['tilesets']
            assert isinstance(self.tilesets, _abctiled.TileSets), \
                "параметр tilesets должен быть объектом класса - {}".format(
                    _abctiled.TileSets.__class__.__name__
                )
            self.create_sets_sprites()
        # если изображение
        elif 'image' in kwargs.keys():
            self.image = kwargs['image']
            assert isinstance(self.image,
                              str), "должна быть строка"
            if 'size' in kwargs.keys():
                assert isinstance(kwargs['size'],
                                  tuple), 'должен быть tuple'
                self.width = kwargs['size'][0]
                self.height = kwargs['size'][1]

                self.create_sub_sprites()

        else:
            raise Exception('отсутствуют параметры')

    def create_sub_sprites(self):
        """
        на основе одного изображения
        """
        self.sub = Sub(image=self.image, width=self.width,

                       height=self.height)
        self._sprites.extend(self.sub.get_sprites())

    def create_sets_sprites(self):
        """
        на основе тайлсетов из сгенерированой карты
        """
        for tset in self.tilesets:
            # если тайлсет (вырезает)
            if isinstance(tset, _abctiled.ImageSet):
                image = tset.image
                w = tset.tilewidth
                h = tset.tileheight
                self.sub = Sub(image=image, width=w, height=h)
                self._sprites.extend(self.sub.get_sprites())
            # коллекция изображений
            elif isinstance(tset, _abctiled.TileSet):
                for img in tset.images:
                    self._sprites.append(
                        pygame.image.load(img).convert_alpha())


class TiledMap(_abctiled.AbcTiled):
    """
    класс представляет карту сгенерированую Tiled Map Editor,
    где атрибуты соответствуют ключам словаря сгенерированой карты
    """

    def __init__(self, map_dict: dict, sets_dir: str, **kwargs):
        """
         карта в виде словаря
        :param sets_dir: путь к каталогу с тайлсетами
        :param map_dict:
        :param kwargs:
        """
        super().__init__(map_dict, sets_dir)
        path = os.path.abspath(sets_dir)
        if os.path.isdir(path):
            self.sets_dir = path
        else:
            raise FileNotFoundError(
                "директория - {} не найдена".format(path))

    @property
    def sub_sprites(self):
        """
        последовательность спрайтов созданная на основе тайлсетов
        :return: SubSprites < Surface
        """
        sub = SubSprites(tilesets=self.tilesets)
        return sub

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
    from pumpkin2 import paths

    pygame.init()
    screen = pygame.display.set_mode((10, 10))
    path_map = paths.get_map('level_1')
    maps = TiledMap.load_map(path_map)
    sets_dir = paths.exsets

    tiled_map = TiledMap(maps, sets_dir)
    # получить subsprites можно после  иницализации дисплея screen
    print(tiled_map.sub_sprites)

    # image = paths.get_exsets('set_2x1x64_white.png')
    # sub = Sub(image, 64, 64)
    # print(sub.get_sprites())
    # print(sub.get_sprites())
    # print(sub.get_sprites_back(), 111)

    # print('-------------------')
    # tiled_map = TiledMap(maps, sets_dir)
    # tileset = tiled_map.tilesets
    # sub = SubSprites(tilesets=tileset)
    # print(sub)


