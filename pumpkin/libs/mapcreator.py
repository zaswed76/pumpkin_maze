import pygame
from pygame.sprite import Group
from libs import tiledmap, units
from libs.units import Platform


class MapCreator:
    def __init__(self, json_map: str, tileset_dir: str,
                 screen: pygame.Surface):
        self.screen = screen
        self.tiled_map = tiledmap.TiledParser(json_map, tileset_dir)

        self.image_sprites = self.tiled_map.get_subsprites(
            self.tiled_map.get_id_tiles())
        self.all_layers = Group()

    def create_map(self):
        for layer in self.tiled_map.layers:
            type_name = layer['name']
            data = layer['data']
            group_layer = units.UGroup(type_name)
            self.create_layer(group_layer, data)


    def create_layer(self, group_layer, data):
        x = 0
        y = 0
        step = self.tiled_map.json_map['tilewidth']
        width = step * self.tiled_map.json_map['width']
        for n in data:
            if n:
                image = self.image_sprites[n -1]
                platform = Platform(group_layer.type, self.screen,
                                    image, x,
                                    y)
                group_layer.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
            self.all_layers.add(group_layer)

    def draw_map(self):
        if self.all_layers:
            self.all_layers.draw(self.screen)
        else:
            print(self.all_layers)