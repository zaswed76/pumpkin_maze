import os

import pygame
from pygame.sprite import Group, OrderedUpdates
from libs import tiledmap, units
from libs.units import Platform


class MapCreator:
    def __init__(self, json_map: str, tileset_dir: str,
                 resources_dir: str,
                 ):
        self.resources_dir = resources_dir
        self.screen = None
        self.tiled_map = tiledmap.TiledParser(json_map, tileset_dir)

        self.size_map = self.get_size_map()

        self.image_sprites = self.tiled_map.get_subsprites(
            self.tiled_map.get_id_tiles())
        self.all_layers = units.UGroup('all')
        self.all_images = OrderedUpdates()

    def get_size_map(self):
        w = (
        self.tiled_map.json_map['width'] * self.tiled_map.json_map[
            'tilewidth'])
        h = (
        self.tiled_map.json_map['height'] * self.tiled_map.json_map[
            'tileheight'])
        return (w, h)

    def set_screen(self, screen):
        self.screen = screen

    def create_map(self):
        for layer in self.tiled_map.layers:
            if layer['type'] == 'tilelayer' and layer['visible']:
                type_name = layer['name']
                data = layer['data']
                group_layer = units.UGroup(type_name)
                self.create_layer(group_layer, data)
            elif layer['type'] == 'imagelayer':
                speed = layer.get('properties', {}).get('speed', 0)
                self.create_image(self.get_image_path(layer['image']),
                                  layer.get('offsetx', 0),
                                  layer.get('offsety', 0),
                                  speed)

    def get_image_path(self, image):
        return os.path.join(self.resources_dir,
                            os.path.basename(image))

    def create_image(self, image_pth, x, y, speed):
        bg = units.Background(self.screen, image_pth, x, y, speed)
        self.all_images.add(bg)

    def create_layer(self, group_layer, data):
        x = 0
        y = 0
        step = self.tiled_map.json_map['tilewidth']
        width = step * self.tiled_map.json_map['width']
        for n in data:
            if n:
                image = self.image_sprites[n - 1]
                platform = Platform(group_layer.type, self.screen,
                                    image, x, y, n)
                group_layer.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
            self.all_layers.add(group_layer)

    def draw_map(self):
        self.all_images.draw(self.screen)
        if self.all_layers:
            self.all_layers.draw(self.screen)

        else:
            print(self.all_layers)

    def update(self):
        self.all_images.update()
