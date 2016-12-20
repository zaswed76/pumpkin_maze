import json
import os

from tabulate import tabulate

from libs import subsprite

def print_dict(d: dict):
    for k, v in d.items():
        print(k, v, sep=' = ')
        print('---------------------------')

class TileObjects(list):
    def __init__(self, objects):
        super().__init__()
        self.extend(objects)

    def print(self):
        for n, i in enumerate(self,start=1):
            print(' ---- LayerObject N-{} ----\n'.format(n))

            for k, v in i.items():
                if k == 'objects':
                    print(' <<< objects >>>')
                    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    for l in v:
                        print(l)
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                else:
                    print(k, v, sep=' = ')

                print('--------------------------')
            print('#'*70)

    def __repr__(self):
        return '{}'.format(len(self))

class Layers(list):
    def __init__(self, layers: list):
        super().__init__()
        self.extend(layers)
        self.objects = self.objects_()
    def __repr__(self):
        return 'layers - {}\n{}'.format(len(self), self.names_layers())

    def names_layers(self):
        layers = []
        for l in self:
            layers.append(l['name'])
        return layers

    def objects_(self):
        lst = []
        for l in self:
            if l['type'] == 'objectgroup' and l['visible']:
                lst.append(l)
        return TileObjects(lst)


class TileSets(dict):
    def __init__(self, sets: dict):
        super().__init__()
        self.update(sets)

    def get_set(self):
        return self

    def print(self):
        for set in self:
            for k, v in set.items():
                print(k, v, sep=' = ')
                print('----------------------')
            print('========================================')
            print('''result:
            --- number of key  = {}'''.format(len(set)))
            print('========================================')

class Parser(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def load_map(self, level_map: str) -> dict:
        with open(level_map, "r") as f:
            return json.load(f)

    def print_map(self, dct):
        for k, v in dct.items():
            print(k, v, sep=' = ')
            print('----------------------------')
        print('################')
        print('len = {}'.format(len(self)))

    def print_layers(self, dct):
        for k, v in dct.items():
            if k == 'layers':
                for lay in v:
                    self.print_map(lay)



class Portal(Parser):
    def __init__(self, json_map: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(self.load_map(json_map))
        self.exit_points = self['exit_points']
        self.point_entry = self['point_entry']
        self.input_side = self['input_side']



class TiledParser(Parser):
    def __init__(self, json_map: str, tileset_dir: str, **kwargs):

        """
        создаёт объект карты, объект SubSprite
        :param json_map: str path каталог размещения json карты
        :param tileset_dir: str path каталог размещения tileseta
        """

        super().__init__(**kwargs)
        self.tileset_dir = tileset_dir
        self.json_map = json_map
        # загрузка карты
        self.update(self.load_map(json_map))
        # слои
        self.layers = Layers(self['layers'])

        # [0] парсится карта ТОЛЬКО с одним тайлсетом
        try:
            self.sets = TileSets(self['tilesets'][0])
        except IndexError:
            self.sets = {}
        # объект SubSprite
        if self.sets:
            tiled_pth = self.get_tileset_path()

            self.subsprite = subsprite.SubSprite(
                tiled_pth,
                self['tilewidth'],
                self['tileheight'])

            self.tiled_properties = self['tilesets'][0].get('tileproperties', dict())

    @property
    def map_dir(self):
        return os.path.dirname(self.json_map)

    @property
    def portal_cfg(self):
        map_dir = os.path.dirname(self.json_map)
        return os.path.join(map_dir, 'portals.json')

    @property
    def portal(self):
        cfg = self.portal_cfg
        return Portal(cfg)

    def get_tileset_path(self):
        pth = self.sets.get('image', False)
        if pth:
            return os.path.join(self.tileset_dir, os.path.basename(pth))
        else: return False


    def save_map(self) -> None:
        with open(self.json_map, "w") as f:
            json.dump(self, f)

    def set_portal(self, layer_name):
        for num_layer, layer in enumerate(self['layers']):
            if layer['name'] == layer_name:
                if not self['layers'][num_layer].get('properties'):
                    self['layers'][num_layer]['properties'] = {}
                if not self['layers'][num_layer].get('propertytypes'):
                    self['layers'][num_layer]['propertytypes'] = {}

                self['layers'][num_layer]['properties']['portal'] = True
                self['layers'][num_layer]['propertytypes']['portal'] = 'bool'
                self.save_map()


    def get_subsprites(self, id_tiles: set) -> dict:
        subsprites = {}
        for tile_id in id_tiles:
            subsprites[tile_id] = self.subsprite.get_sprite(tile_id)
        return subsprites

    def get_id_tiles(self) -> set:
        """

        :return: id всех задействованых тайлов
        """
        tiles = set()
        for lay in self.layers:
            if lay['type'] == 'tilelayer' and lay['visible']:
                for tile in lay['data']:
                    if tile:
                        # сдвигаем на один назад (в json карте отсчёт от 1)
                        tiles.add(tile - 1)
        return tiles


if __name__ == '__main__':
    from pumpkin import paths

    pth_map = os.path.join(paths.maps, '1', 'tiled_map.json')
    tiled = TiledParser(pth_map, paths.tilesets)
    # tiled.print_map()
    tiled.print_layers(tiled)
    # print(tiled.sets.get_set())
    # print(tiled.get_subsprites(tiled.get_id_tiles()))
