# -*- coding: utf-8 -*-


from pumpkin2 import paths
from pumpkin2.tiledlib import subsprite

tilesets= [
        {
         "columns":4,
         "firstgid":1,
         "image":"set_4x3x32_transparent.png",
         "imageheight":96,
         "imagewidth":128,
         "tilecount":12,
         "tileheight":32,
         "tilewidth":32
        },
        {
         "columns":2,
         "firstgid":13,
         "image":"set_2x1x64transparent.png",
         "imageheight":64,
         "imagewidth":128,
         "tilecount":2,
         "tileheight":64,
         "tilewidth":64
        }]

class Sub:
    def __init__(self, tilesets):
        self.tilesets = tilesets
        self.sprites = []

    def __getitem__(self, key):
        """
        """
        if isinstance(key, slice):
            # noinspection PyTypeChecker
            return self.sprites[key.start - 1: key.stop - 1]
        else:
            return self.sprites[key-1]


    def create_sprites(self):
        for tset in tilesets:
            image = paths.get_exsets(tset['image'])
            w = tset['tilewidth']
            h = tset['tileheight']
            sub = subsprite.SubSprite(image, w, h)
            self.sprites.extend(sub.get_sprites())

    def __repr__(self):
        return str(self.sprites)


if __name__ == '__main__':
    import pygame
    pygame.init()
    screen = pygame.display.set_mode(
        (500, 500))
    sub = Sub(tilesets)
    sub.create_sprites()
    print(sub)