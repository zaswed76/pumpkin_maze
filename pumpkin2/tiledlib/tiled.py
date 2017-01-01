
import pygame
from pumpkin2.tiledlib import abctiled


class _SubSprite:
    def __init__(self, image, width, height):
        self.image = image
        self.height = height
        self.width = width
        self.sprite = pygame.image.load(image).convert_alpha()
        self.sprite_rect = self.sprite.get_rect()
        self.w_count = self.sprite_rect.width // self.width
        self.h_count = self.sprite_rect.height // self.height

    def get_coord(self, n, width, height, w_count):
        n_y = n // w_count
        x = width * int(n - (n_y * w_count))
        y = height * n_y
        return x, y

    def get_sprite(self, n):
        x, y = self.get_coord(n, self.width, self.height,
                              self.w_count)
        return self.sprite.subsurface((x, y, self.width, self.height))

    def get_sprites(self, s=0, count=None):
        if count is None:
            f = self.w_count * self.h_count
        else:
            f = s + count + 1
        lst = []
        for x in range(s, f):
            lst.append(self.get_sprite(x))
        return lst

    def get_sprites_back(self, n=None):
        if n is None:
            n = int(self.w_count)
        lst = list(range(n))
        lst.extend(sorted(range(n), reverse=1))
        return [self.get_sprite(x) for x in lst]

    def get_sprite_time(self, s, t):
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


class SubSprites:
    def __init__(self, **kwargs):
        """

        :rtype: SubSprites
        """
        self.__sprites = []
        self.value = 0

        if 'tilesets' in kwargs:
            self.tilesets = kwargs['tilesets']
            assert isinstance(self.tilesets, abctiled.TileSets), \
                "параметр tilesets должен быть объектом класса - {}".format(
                    abctiled.TileSets.__class__.__name__
                )
            self.create_sets_sprites()
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
        self.sub = _SubSprite(image=self.image, width=self.width,

                         height=self.height)
        self.__sprites.extend(self.sub.get_sprites())

    def create_sets_sprites(self):
        for tset in self.tilesets:
            image = tset.image
            w = tset.tilewidth
            h = tset.tileheight
            self.sub = _SubSprite(image=image, width=w, height=h)
            self.__sprites.extend(self.sub.get_sprites())

    def __iter__(self): # Возвращает итератор в iter()
        return self

    def __next__(self): # Возвращает квадрат в каждой итерации
        if self.value == len(self.__sprites): # Также вызывается функцией next
            raise StopIteration

        z = self.__sprites[self.value]
        self.value += 1
        return z

    def __getitem__(self, key):
        """
        """
        if isinstance(key, slice):
            # noinspection PyTypeChecker
            assert key.start > 0, "!!!"
            return self.__sprites[key.start - 1: key.stop - 1]
        else:
            print(key, 444)
            assert key > 0, 'Index sprites list starts with 1'
            assert key <= len(self.__sprites), \
                '''Length is the list of sprites - {}'''.format(
                    len(self.__sprites))
            return self.__sprites[key - 1]

    def __add__(self, other):
        if isinstance(other, SubSprites):
            self.__sprites.extend(other)
            return self.__sprites
        else:
            raise TypeError('слагаемое должно быть объктом класса SubSprites')


    def __len__(self):
        return len(self.__sprites)

    def __repr__(self):
        return str(self.__sprites)

class Tiled(abctiled.AbcTiled):
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
        self.sets_dir = sets_dir

    @property
    def sub_sprites(self):
        sub = SubSprites(tilesets=self.tilesets)
        return sub

    @property
    def size(self):
        w = self.width * self.tilewidth
        h = self.height * self.tileheight
        return (w, h)


if __name__ == '__main__':
    from pumpkin2 import paths
    path_map = paths.get_map('level_1')
    maps = Tiled.load_map(path_map)
    sets_dir = paths.exsets
    tiled_map = Tiled(maps, sets_dir)
    print(tiled_map.tilesets)

