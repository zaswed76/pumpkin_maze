import json

import pygame
from pygame.sprite import Sprite
from platform import Platform
from libs import subsprite
from tileset_game import paths

class AbsSprite(Sprite):
    def __init__(self, screen, image, alpha=False, *groups):
        super().__init__(*groups)
        if alpha:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.image.load(image).convert()
        self.screen = screen
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Background(AbsSprite):
    def __init__(self, screen, image, alpha=False, *groups):
        super().__init__(screen, image, alpha, *groups)


class Layers:
    def __init__(self):
        """

        """
        pass


class MapParser:
    def __init__(self, level_map):
        self.level_map = self.get_level(level_map)
        self.layers = self.level_map['layers']
        self.tilewidth = self.level_map['tilesets'][0]['tilewidth']
        self.tileheight = self.level_map['tilesets'][0]['tileheight']
        self.set_image = self.level_map['tilesets'][0]['image']
        print(os.path.dirname(self.set_image))
        print(os.path.abspath(self.set_image))
        # print(os.path.join(paths.root, os.path.abspath(self.set_image)))
        self.width = self.level_map['width']
        self.bg_image = None
        self.tile_layers = []

        self.parse_layers()

    def parse_layers(self):
        for layer in self.layers:
            if layer['type'] == 'imagelayer':
                self.bg_image = layer['image']
            elif layer['type'] == 'tilelayer':
                self.tile_layers.append(layer['data'])

    def get_level(self, level_map):
        with open(level_map, "r") as f:
            return json.load(f)

    def print(self):
        for k, i in self.level_map.items():
            print(k, i, sep=' = ')

    def print_layers(self):
        for lay in self.level_map['layers']:
            print(lay)
            print('------------------')


class LevelMap:
    def __init__(self, level, screen, all_layers):
        self.all_layers = all_layers
        self.image_background = None
        self.screen = screen
        self.map_parser = MapParser(level)
        self.subsprite = subsprite.SubSprite(
            self.map_parser.set_image,
            self.map_parser.tilewidth,
            self.map_parser.tileheight)
        self.images_subsprite = self.subsprite.get_sprites()



    def create_background(self, group):
        bg = Background(self.screen, self.map_parser.bg_image)
        group.add(bg)
        self.all_layers.add(group)


    def draw_layers(self):
        self.all_layers.draw(self.screen)

    def create_map(self, *groups):
        for group, data in zip(groups, self.map_parser.tile_layers):
            self.creare_layer(group, data)


    def creare_layer(self, group, data):
        x = 0
        y = 0
        step = self.map_parser.tilewidth
        width = step * self.map_parser.width

        for n in data:
            if n:
                image = self.images_subsprite[n-1]
                platform = Platform(self.screen, image, x, y)
                group.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
            self.all_layers.add(group)



if __name__ == '__main__':
    import os
    import paths
    import pygame
    from pygame.sprite import Group
    from libs import subsprite

    pygame.init()
    screen = pygame.display.set_mode((150, 150))
    pth_map = os.path.join(paths.maps, 'new2.json')
    print(paths.root)
    print(pth_map)
    # mp = LevelMap(pth_map, screen, Group())
    # print(mp.map_parser.level_map['tilesets'])
    # mp.map_parser.print()
    # print(mp.map_parser.tile_layers)
    # print(mp.map_parser.bg_image)
    # mp.create_map()
