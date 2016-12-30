# -*- coding: utf-8 -*-


from pumpkin2 import paths
from pumpkin2.tiledlib import subsprite, tiled
from pumpkin2.tiledlib import tiled as tl


# tilesets= [
#         {
#          "columns":4,
#          "firstgid":1,
#          "image":"set_4x3x32_transparent.png",
#          "imageheight":96,
#          "imagewidth":128,
#          "tilecount":12,
#          "tileheight":32,
#          "tilewidth":32
#         },
#         {
#          "columns":2,
#          "firstgid":13,
#          "image":"set_2x1x64transparent.png",
#          "imageheight":64,
#          "imagewidth":128,
#          "tilecount":2,
#          "tileheight":64,
#          "tilewidth":64
#         }]




if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode(
        (500, 500))
    set_dir = paths._exsets
    tmap = tl.Tiled.load_map(paths.get_map('level_1'))

    tiled = tl.Tiled(tmap, set_dir)

    for i in tiled.tilesets:
        print(i)
    print(tiled.tilesets)
    sub = TileSprite(tiled.tilesets)
    sub.create_sprites()
    print(sub)
