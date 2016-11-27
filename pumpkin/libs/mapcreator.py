import os

import pygame
from pygame.sprite import Group, OrderedUpdates
from libs import tiledmap, units
from libs.units import Platform


class LevelCreator:
    def __init__(self, screen: pygame.Surface, json_map: str,
                 tileset_dir: str,
                 resources_dir: str
                 ):
        self.resources_dir = resources_dir
        self.screen = screen
        self.tiled_map = tiledmap.TiledParser(json_map, tileset_dir)

        self.size_map = self.get_size_map()

        self.image_sprites = self.tiled_map.get_subsprites(
            self.tiled_map.get_id_tiles())
        self.level = units.Level()
        self.all_images = OrderedUpdates()
        self.bg_type = None

    def set_bg_type(self, type):
        self.bg_type = type

    def get_size_map(self):
        w = (
            self.tiled_map['width'] * self.tiled_map['tilewidth'])
        h = (
            self.tiled_map['height'] * self.tiled_map['tileheight'])
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
            elif layer['type'] == 'imagelayer' and layer['visible']:
                speed = layer.get('properties', {}).get('speed', 0)
                self.create_image(self.get_image_path(layer['image']),
                                  layer.get('offsetx', 0),
                                  layer.get('offsety', 0),
                                  speed)
            elif layer['type'] == 'objectgroup' and layer['visible']:
                self.create_object(self.screen, layer)

    def get_image_path(self, image):
        return os.path.join(self.resources_dir,
                            os.path.basename(image))

    def create_image(self, image_pth, x, y, speed):
        bg = self.bg_type(self.screen, image_pth, x, y, speed)
        self.level[image_pth] = bg

    def create_layer(self, group_layer, data):
        x = 0
        y = 0
        step = self.tiled_map['tilewidth']
        width = step * self.tiled_map['width']
        for n in data:
            if n:
                gid = n - 1
                image = self.image_sprites[gid]
                platform = Platform(group_layer.type, self.screen,
                                    image, x, y, gid,
                                    self.tiled_map.tiled_properties.get(str(gid), dict()))
                group_layer.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
        self.level[group_layer.type] = (group_layer)

    def create_object(self, screen, layer):
        for obj in layer['objects']:
            figure = units.Rect(screen, **obj)
            self.level[figure.name] = figure

    def draw_tiles(self):

        if self.level:
            self.level.draw(self.screen)

        else:
            print(self.level)

    def fill(self):
        self.screen.fill(pygame.Color(
            self.tiled_map.get('backgroundcolor', 'black')))


class Levels(list):
    def __init__(self, screen: pygame.Surface, map_dir: str,
                 tileset_dir: str, resources_dir: str, config,
                 map_format='.json'):
        super().__init__()
        self.screen = screen
        self.resources_dir = resources_dir
        self.tileset_dir = tileset_dir
        self.map_format = map_format
        self.map_dir = map_dir
        self.included_level = config.included_level
        self.maps = self.get_maps()
        self.bg_type = units.Background

    def get_maps(self) -> list:
        """
        составляет список путей к картам на основании списка config.included_level
        :return: list < str
        """
        maps = []
        for lev_name in self.included_level:
            path = os.path.join(self.map_dir,
                                str(lev_name) + self.map_format)
            # если карта существует
            if os.path.isfile(path):
                maps.append(path)
            else:
                print('путь - {} не найден'.format(path))
                print('---------------------------------')
        return maps

    def create_levels(self):

        """
        создаёт все уровни
        :return:
        """
        if not self.maps:
            return None
        for map in self.maps:
            # создать уровень
            level = LevelCreator(self.screen, map, self.tileset_dir,
                                 self.resources_dir)
            level.set_bg_type(self.bg_type)
            level.create_map()
            self.append(level)

    def draw(self, level: int):
        """
         отрисовывает уровень на поверхности pygame.Surface
        :param level: номер уровня
        """
        # todo что зачем?
        self[level].fill()

        self[level].draw_tiles()

    def set_bg_type(self, bg_type: units.AbsSprite):
        """

        :param bg_type: units.AbsSprite
        """
        self.bg_type = bg_type
