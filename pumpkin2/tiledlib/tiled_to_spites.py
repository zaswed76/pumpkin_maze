# -*- coding: utf-8 -*-


from pumpkin2 import paths
from pumpkin2.tiledlib import tiled as tl
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
        sub = _SubSprite(image=self.image, width=self.width,
                         height=self.height)
        self.__sprites.extend(sub.get_sprites())

    def create_sets_sprites(self):
        for tset in self.tilesets:
            image = tset.image
            w = tset.tilewidth
            h = tset.tileheight
            sub = _SubSprite(image=image, width=w, height=h)
            self.__sprites.extend(sub.get_sprites())

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
        self.__sprites.extend(other)
        return self.__sprites


    def __len__(self):
        return len(self.__sprites)

    def __repr__(self):
        return str(self.__sprites)


if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode(
        (500, 500))
    set_dir = paths.exsets
    set_image = paths.get_exsets('set_2x1x64transparent.png')
    tmap = tl.Tiled.load_map(paths.get_map('level_1'))

    tiled = tl.Tiled(tmap, set_dir)

    sub = SubSprites(image=set_image, size=(64, 64))
    print(sub)
    print('-------------------------')
    sub2 = SubSprites(tilesets=tiled.tilesets)
    sub = sub + sub2
    print(sub)
