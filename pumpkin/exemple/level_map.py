import json
import os
from pygame import init, display, sprite
from pumpkin.libs.subsprite import SubSprite
from pumpkin.libs.game_groups import ImagePlatform, Background

def get_map_files(direct):
    return [os.path.join(direct, p) for p in os.listdir(direct)]


class MapParser:
    def __init__(self, level_map):
        self.level_map = self.get_level(level_map)
        self.layers = self.level_map['layers']
        self.tilewidth = self.level_map['tilesets'][0]['tilewidth']
        self.tileheight = self.level_map['tilesets'][0]['tileheight']
        self.set_image = self.level_map['tilesets'][0]['image']

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
            print('-----------------------------------')

    def print_layers(self):
        for lay in self.level_map['layers']:
            print(lay)
            print('------------------')


class LevelMap(list):
    def __init__(self, level, screen, all_layers, imgset_dir=None):

        super().__init__()
        self.imgset_dir = imgset_dir

        self.all_layers = all_layers

        self.screen = screen
        self.map_parser = MapParser(level)
        self.image_background = self.get_bg_path(
            self.map_parser.bg_image)
        if self.imgset_dir is None:
            self.image_set = self.map_parser.set_image
        else:
            self.image_set = self.get_fotoset_path(
                self.map_parser.set_image)
        self.subsprite = SubSprite(
            self.image_set,
            self.map_parser.tilewidth,
            self.map_parser.tileheight)
        self.images_subsprite = self.subsprite.get_sprites()

    def get_bg_path(self, pth):
        if pth is not None:
            return os.path.join(self.imgset_dir, os.path.basename(pth))

    def get_fotoset_path(self, pth):
        return os.path.join(self.imgset_dir, os.path.basename(pth))

    def create_background(self, group):
        if self.map_parser.bg_image is not None:
            bg = Background(self.screen, self.image_background)
            group.add(bg)
            self.all_layers.add(group)

    def draw_layers(self):

        self.all_layers.draw(self.screen)

    def create_map(self, **groups):
        for group, data in zip(groups.values(), self.map_parser.tile_layers):
            self.creare_layer(group, data)

    def creare_layer(self, group, data):
        x = 0
        y = 0
        step = self.map_parser.tilewidth
        width = step * self.map_parser.width
        print(data)
        for n in data:
            if n:
                image = self.images_subsprite[n - 1]
                platform = ImagePlatform(group.name, self.screen, image, x,
                                         y)
                group.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
            self.all_layers.add(group)

    def empty(self):
        self.all_layers.empty()


class Levels(list):
    def __init__(self, maps, screen, resource,  **groups):
        super().__init__()
        self.bg_group = None
        self.resource = resource
        self.groups = groups
        self.screen = screen
        self.maps = maps
        self.create_levels()

    def create_levels(self):
        for map in self.maps:
            level = self.create_level(map, self.screen)
            self.append(level)

    def create_level(self, mp, screen):
        all_group = sprite.LayeredUpdates()
        level = LevelMap(mp, screen, all_group,
                         imgset_dir=self.resource)
        if self.bg_group is not None:
            level.create_background(self.bg_group)
        level.create_map(**self.groups)
        return all_group


if __name__ == '__main__':
    import os
    from pumpkin import paths
    import pygame
    from pygame.sprite import Group
    from libs import subsprite

    init()
    screen = display.set_mode((150, 150))
    pth_map = os.path.join(paths.maps, 'map1.json')

    mp = MapParser(pth_map)
    lay = mp.level_map['layers'][0]
    prop = lay.get('properties')
    mp.print()
    print()
