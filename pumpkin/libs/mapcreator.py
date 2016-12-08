import os

import pygame
from pygame.sprite import Group, OrderedUpdates
from libs import tiledmap, game_groups, sprites
from libs import color as _color
from libs.sprites import CreateImagePlatform, CreateThings, \
    CreateFigure


def print_dict(d: dict):
    for k, v in d.items():
        print(k, v, sep=' = ')
        print('---------------------------')


class Properties(dict):
    def __init__(self):
        super().__init__()

    def update(self, E=None, options=None, **F):
        if options is not None:
            print(222)
            super().update({k: F.get(k) for k in options})
        else:
            super().update(**F)


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
        self.all_layers = game_groups.AllLayers()
        self.all_images = OrderedUpdates()
        self.bg_type = None
        self.name = os.path.splitext(os.path.basename(json_map))[0]

    def set_bg_type(self, type):
        """

        :param type: ссылка на КЛАСС - наследник sprites.AbsBackGround
        """
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
            # пользовательские настройки слоя
            user_properties = layer.get('properties', {})
            # тип слоя (sprites.GameObject)
            class_name = user_properties.get('class')

            name_layer = layer['name']
            group = game_groups.OrderedGroupLayer(
                name_layer, class_name, user_properties)
            if layer['type'] == 'tilelayer' and layer['visible']:
                data = layer['data']
                self.create_layer(group, data)
            elif layer['type'] == 'imagelayer' and layer['visible']:
                # todo переделать вызов create_image()
                speed = user_properties.get('speed', 0)
                self.create_image(group,
                                  self.get_image_path(layer['image']),
                                  layer.get('offsetx', 0),
                                  layer.get('offsety', 0),
                                  speed)
            elif layer['type'] == 'objectgroup' and layer['visible']:
                self.create_figure_objects(group, self.screen,
                                           layer)

    def get_image_path(self, image):
        """

        :param image: относительный путь к изображению
        :return: абсалютный путь к изображению
        """
        return os.path.join(self.resources_dir,
                            os.path.basename(image))

    def create_image(self, group, image_pth, x, y, speed):
        #
        bg = self.bg_type(group, self.screen, image_pth, x, y, speed)


        self.all_layers[group.name] = (group)

    def create_layer(self, group_layer, data):
        x = 0
        y = 0
        step = self.tiled_map['tilewidth']
        width = step * self.tiled_map['width']
        for count, n in enumerate(data):
            if n:
                gid = n - 1
                image = self.image_sprites[gid]
                portal = group_layer.doors_portal.get(count)
                tiled_properties = self.tiled_map.tiled_properties.get(
                    str(gid), dict())
                group_properties = group_layer.properties
                if group_properties.get(
                        'class') == game_groups.GameObject.Thing:
                    CreateThings(group_layer, self.screen,
                                 image, x, y, count,
                                 tiled_properties)

                else:
                    CreateImagePlatform(group_layer, self.screen,
                                        image, x, y, count,
                                        tiled_properties, portal)

                x += step
            else:
                x += step
            if x == width:
                x = 0
                y += step
        self.all_layers[group_layer.name] = (group_layer)

    def create_figure_objects(self, group, screen, layer):
        # ключи которые включены в layer_properties
        layer_properties_opts = ['offsetx', 'offsety', 'color',
                                 'type', 'opacity',
                                 'name', 'visible']
        layer_properties = Properties()
        layer_properties.update(options=layer_properties_opts,
                                **layer)
        # пользовательские свойства слоя
        user_layer_properties = layer.get('properties', {})
        # все фигуры
        objects = layer['objects']
        for object in objects:
            CreateFigure(group, screen, object, layer_properties,
                         user_layer_properties)

        self.all_layers[group.name] = group

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
        return 'level - {}'.format(self.all_layers)


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
        # todo переделать устанвку типа Background
        self.bg_type = sprites.Background

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

    def create_levels(self, level):

        """
        создаёт все уровни
        :return:
        """
        if not self.maps:
            return None
        map = self.maps[level]
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
        self[0].fill()
        self[0].draw_layers()

    def set_bg_type(self, bg_type: sprites.AbsBackGround):
        """

        :param bg_type: units.AbsSprite
        """
        self.bg_type = bg_type
