import json
import os
from collections import namedtuple


class TsetError(Exception):
    def __init__(self, value, mess: str, *args):
        self.args = args
        self.mess = mess
        self.value = value

    def __str__(self):
        return self.mess.format(self.value, *self.args)


err_message_options = """
тайл сет - {} должен иметь
пользовательский параметр - {}
"""

err_message_properties = """
тайл сет - {} должен иметь
пользовательский параметр
"""
err_message_valid_type = """
тайл сет - {}:
пользовательский параметр {} может иметь одно из этих значений:
{}
"""


class _Tiled:
    def __init__(self):
        pass

    @property
    def empty_options(self):
        return [k for k, v in self.__dict__.items() if v is None]

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)


class TileSet(_Tiled):
    ''' коллекция изображений '''

    def __init__(self, tset: dict, **kwargs):
        # todo надо ли переделывать в словарь (универсальнее?)
        super().__init__()
        self.sets_dir = kwargs['sets_dir']
        self.columns = tset.get("columns")
        self.firstgid = tset.get("firstgid")
        self.margin = tset.get("margin")
        self.name = tset.get("name")
        self.properties = tset.get("properties")
        self.spacing = tset.get("spacing")
        self.tilecount = tset.get("tilecount")
        self.tileheight = tset.get("tileheight")
        self.tileproperties = tset.get("tileproperties")
        self.tilepropertytypes = tset.get("tilepropertytypes")
        self.tiles = tset.get("tiles")

        self.tilewidth = tset.get("tilewidth")

    @property
    def images(self):
        """

        :return: list < str список путей
        """
        images = []
        tiles = sorted(self.tiles.items(), key=lambda item: item[0])
        for img in tiles:
            paths = os.path.join(self.sets_dir,
                                 os.path.basename(img[1]['image']))
            if not os.path.isfile(paths):
                raise FileNotFoundError('нет картинки')
            else:
                images.append(paths)
        return images

    def __repr__(self):
        s = super().__repr__()
        z = '\n' + '\n'.join(str(x) for x in self.tiles.values())
        return " - ".join((s, z))


class ImageSet(_Tiled):
    """ набор тайлов в одном изображении"""

    def __init__(self, tset: dict, **kwargs):
        super().__init__()
        self.sets_dir = kwargs['sets_dir']
        self.columns = tset.get("columns")
        self.firstgid = tset.get("firstgid")
        self._image = tset.get("image")
        self.imageheight = tset.get("imageheight")
        self.imagewidth = tset.get("imagewidth")
        self.margin = tset.get("margin")
        self.name = tset.get("name")
        self.properties = tset.get("properties")
        self.tilecount = tset.get("tilecount")
        self.tileheight = tset.get("tileheight")
        self.tileoffset = tset.get("tileoffset")
        self.tilewidth = tset.get("tilewidth")

    @property
    def image(self):
        paths = os.path.join(self.sets_dir,
                             os.path.basename(self._image))
        if not os.path.isfile(paths):
            raise FileNotFoundError('файл не найден')
        else:
            return paths

    def __repr__(self):
        s = super().__repr__()
        z = '{}'.format(self.image)
        return " - ".join((s, z))


class TileSets:
    type_sets = dict(image=ImageSet, tile=TileSet)

    def __init__(self, sets: list, **kwargs):
        """

        :param sets: список словарей tilesets
        :param kwargs: set_dir < str; путь к каталогу с сетами
        """
        self.set_dir = kwargs['sets_dir']
        self._sets = []
        self.__create_sets(sets)

    @property
    def sets(self):
        """

        :return: list < type: type_sets
        """
        return self._sets

    @property
    def count(self):
        """

        :return: list < namedtuple: елементов в каждом тайлсете
        """
        Count = namedtuple('Tilesets', ['name', 'length'])
        count = []
        for s in self._sets:
            count.append(Count(s.name, s.tilecount))
        return count

    def __create_sets(self, sets):
        for tset in sets:
            try:
                tset_properties = tset['properties']
            except KeyError:
                raise TsetError(tset['name'], err_message_properties)
            try:
                cls_name = tset_properties['class']
            except KeyError:
                raise TsetError(tset['name'], err_message_options,
                                'class')
            if not cls_name in self.type_sets.keys():
                raise TsetError(tset['name'], err_message_valid_type,
                                'class', tuple(self.type_sets.keys()))
            self.sets.append(
                # создаём объекты тайлсетов
                self.type_sets[cls_name](tset,
                                         sets_dir=self.set_dir))

    def __getitem__(self, item):
        return self.sets[item]

    def __len__(self):
        return len(self.sets)

    def __repr__(self):
        return "\n----------\n".join([str(x) for x in self.sets])


class AbcTiled(_Tiled):
    """
    обёртка над словарём предсставляющем карту Tiled Map Editor
    """

    def __init__(self, map_dict: dict, sets_dir):
        # all layers
        """

        :param map_dict: www
        """

        super().__init__()

        self.sets_dir = sets_dir
        self.layers = map_dict.get("layers")
        # Stores the next available ID for new objects.
        self.nextobjectid = map_dict.get("nextobjectid")
        self.orientation = map_dict.get("orientation")
        self.renderorder = map_dict.get("renderorder")
        self.tileheight = map_dict.get("tileheight")
        self.tilesets = TileSets(map_dict.get("tilesets", []),
                                 sets_dir=self.sets_dir)
        self.tilewidth = map_dict.get("tilewidth")
        self.tilewidth = map_dict.get("tilewidth")
        self.version = map_dict.get("version")
        self.width = map_dict.get("width")
        self.properties = map_dict.get("properties")
        self.backgroundcolor = map_dict.get("backgroundcolor")
        self.propertytypes = map_dict.get("propertytypes")
        self.height = map_dict.get("height")

    def __str__(self):
        return '''  class - {}
  layers - {}
  user_properties - {}
  width - {} tiles
  height - {} tiles
  count sets - {} sets
  '''.format(self.__class__.__name__,
             len(self.layers),
             self.properties,
             self.width,
             self.height,
             len(self.tilesets)
             )

    @staticmethod
    def load_map(pth_map: str) -> dict:
        """

        :param pth_map: path to json map
        :return: map < dict
        """
        with open(pth_map, "r") as f:
            return json.load(f)


if __name__ == '__main__':
    from pumpkin2 import paths

    path_map = paths.get_map('level_1')
    maps = AbcTiled.load_map(path_map)

    # print_dict(maps)
    # layer = maps['layers'][0]
    # print_dict(layer)
    # objects = layer['objects']
    # print_list(objects)
    # print('#######################')
    # print_sets(maps['layers'][0]['objects'])
