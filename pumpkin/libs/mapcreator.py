import os

import pygame
from pygame.sprite import Group, OrderedUpdates
from libs import tiledmap, units, color
from libs import color as _color
from libs.units import Platform

def print_dict(d: dict):
    for k, v in d.items():
        print(k, v, sep=' = ')
        print('---------------------------')


class Level:
    def __init__(self, screen: pygame.Surface, json_map: str,
                 tileset_dir: str,
                 resources_dir: str
                 ):
        self.n = 0
        self.resources_dir = resources_dir
        self.screen = screen
        self.tiled_map = tiledmap.TiledParser(json_map, tileset_dir)

        self.size_map = self.get_size_map()

        # если есть тайлсет
        if self.tiled_map.sets:
            self.image_sprites = self.tiled_map.get_subsprites(
                self.tiled_map.get_id_tiles())
        self.all_layers = units.AllLayers()
        self.all_images = OrderedUpdates()
        self.bg_type = None
        self.name = os.path.splitext(os.path.basename(json_map))[0]

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
            properties = layer.get('properties', {})
            class_name = properties.get('class')
            name_layer = layer['name']

            if layer['type'] == 'tilelayer' and layer['visible']:
                data = layer['data']
                group_layer = units.UGroup(name_layer, class_name)
                self.create_layer(group_layer, data)
            elif layer['type'] == 'imagelayer' and layer['visible']:
                speed = properties.get('speed', 0)
                self.create_image(self.get_image_path(layer['image']),
                                  layer.get('offsetx', 0),
                                  layer.get('offsety', 0),
                                  speed)
            elif layer['type'] == 'objectgroup' and layer['visible']:
                group_layer = units.UGroup(name_layer, class_name)
                self.create_object(group_layer, self.screen, layer)

    def get_image_path(self, image):
        return os.path.join(self.resources_dir,
                            os.path.basename(image))

    def create_image(self, image_pth, x, y, speed):
        bg = self.bg_type(self.screen, image_pth, x, y, speed)

        self.all_layers[image_pth] = bg

    def create_layer(self, group_layer, data):
        x = 0
        y = 0
        step = self.tiled_map['tilewidth']
        width = step * self.tiled_map['width']
        for n in data:
            if n:
                gid = n - 1
                image = self.image_sprites[gid]
                platform = Platform(group_layer.class_name, self.screen,
                                    image, x, y, gid,
                                    self.tiled_map.tiled_properties.get(
                                        str(gid), dict()))
                group_layer.add(platform)
                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step

        self.all_layers[group_layer.name] = (group_layer)

    def create_object(self, group_layer, screen, layer):
        for obj in layer['objects']:
            layer_figure_type = layer.get('properties', {}).get('figure_type', False)
            object_figure_type = obj.get('type', False)
            if object_figure_type:
                figure_type = object_figure_type
            else:
                figure_type = layer_figure_type
            if figure_type:
                # передаём цвет в порядке приоритета
                color = _color.get_color(obj.get('properties', dict()).get('color'), layer.get('color'))
                if color:
                    figure = units.FigureFabric(screen, color, figure_type, **obj)
                    group_layer.add(figure())
                else:  print('объкт - {} не имеет цвета'.format(obj.get('type')))
            else: print('объкт - "{}" не имеет типа'.format(obj.get('type')))

        self.all_layers[group_layer.name] = group_layer



    def draw_layers(self):
        if self.all_layers:
            self.all_layers.draw(self.screen)
        else:
            self.n += 1
            if self.n < 3:
                print('все слои пусты', 'method - draw_layers')
                print(self.all_layers)

    def fill(self):
        self.screen.fill(pygame.Color(
            self.tiled_map.get('backgroundcolor', 'black')))

    def __repr__(self):
        return 'level - {}'.format(self.name)


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
            level = Level(self.screen, map, self.tileset_dir,
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
        self[level].draw_layers()

    def set_bg_type(self, bg_type: units.AbsSprite):
        """

        :param bg_type: units.AbsSprite
        """
        self.bg_type = bg_type
