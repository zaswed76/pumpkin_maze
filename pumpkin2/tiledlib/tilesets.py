import json
import os
from collections import namedtuple


__all__ = ["ImageCollection", "TileSet", "TileSets"]

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
def get_path(dir_name, base_name):
    # todo а если несколько файлов
    """
     сканируем все папки каталога и выдаём полный путь к тайл сету
    :param dir_name: путь к корнюевой папке программы
    :param base_name: базовое имя тайлсета
    :return:
    """

    lst = []
    for root, dirs, files in os.walk(dir_name):  # пройти по директории рекурсивно
        for name in files:
            fullname = os.path.join(root, name)  # получаем полное имя файла
            if base_name in fullname:
                lst.append(fullname) # делаем что-нибудь с ним
    return lst[0]


class _Tiled:
    def __init__(self):
        pass

    @property
    def empty_options(self):
        return [k for k, v in self.__dict__.items() if v is None]

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)


class ImageCollection(_Tiled):
    ''' коллекция изображений '''

    def __init__(self, tset: dict, **kwargs):
        super().__init__()
        self.root = kwargs['root']
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


    def image(self, img):
        print(img)
        base = os.path.basename(img) # базовое имя
        image = get_path(self.root, base) # сканируем все папки
        return image

    @property
    def images(self):
        """

        :return: list < str список путей
        """
        images = []
        tiles = sorted(self.tiles.items(), key=lambda item: item[0])
        for img in tiles:
            paths = self.image(img[1]['image'])
            if not os.path.isfile(paths):
                raise FileNotFoundError('нет картинки')
            else:
                images.append(paths)
        return images

    def __repr__(self):
        s = super().__repr__()
        z = '\n' + '\n'.join(str(x) for x in self.tiles.values())
        return " - ".join((s, z))


class TileSet(_Tiled):
    """ набор тайлов в одном изображении"""

    def __init__(self, tset: dict, **kwargs):
        super().__init__()
        self.root = kwargs['root']
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
        base = os.path.basename(self._image) # базовое имя
        image = get_path(self.root, base) # сканируем все папки
        return image

class TileSets:
    type_sets = dict(tileset=TileSet, collection=ImageCollection)

    def __init__(self, sets: list, root, **kwargs):
        """

        :param sets: список словарей tilesets
        :param kwargs: set_dir < str; путь к каталогу с сетами
        """
        self.root = root

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
            # noinspection PyCallingNonCallable
            self.sets.append(
                # создаём объекты тайлсетов
                self.type_sets[cls_name](tset,
                                         root=self.root))

    def __getitem__(self, item):
        return self.sets[item]

    def __len__(self):
        return len(self.sets)

    def __repr__(self):
        return "\n----------\n".join([str(x) for x in self.sets])






if __name__ == '__main__':
    from pumpkin2 import paths

    path_map = paths.get_map('level_1')

