import json
import os

from libs import subsprite

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
        return self[0]

    def print(self):
        for set in self:
            for k, v in set.items():
                print(k, v, sep=' = ')
                print('----------------------')
            print('========================================')
            print('''result:
            --- number of key  = {}'''.format(len(set)))
            print('========================================')


class TiledParser(dict):
    def __init__(self, json_map: str, tileset_dir: str, **kwargs):

        """
        создаёт объект карты, объект SubSprite
        :param json_map: str path каталог размещения json карты
        :param tileset_dir: str path каталог размещения tileseta
        """

        super().__init__(**kwargs)
        self.tileset_dir = tileset_dir
        # загрузка карты
        self.update(self.load_map(json_map))
        # слои
        self.layers = Layers(self['layers'])

        # [0] парсится карта ТОЛЬКО с одним тайлсетом
        try:
            self.sets = TileSets(self['tilesets'][0])
        except IndexError:
            pass
        # объект SubSprite
        self.subsprite = subsprite.SubSprite(
            self.get_tileset_path(),
            self['tilewidth'],
            self['tileheight'])

        self.tiled_properties = self['tilesets'][0].get('tileproperties', dict())


    def get_tileset_path(self):
        pth = self.sets['image']
        return os.path.join(self.tileset_dir, os.path.basename(pth))


    def load_map(self, level_map: str) -> dict:
        with open(level_map, "r") as f:
            return json.load(f)

    def print_map(self):
        for k, v in self.items():
            print(k, v, sep=' = ')
            print('----------------------------')
        print('################')
        print('len = {}'.format(len(self)))

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

    pth_map = os.path.join(paths.maps, '3.json')
    tiled = TiledParser(pth_map, paths.tilesets)
    # tiled.print_map()
    print(tiled.layers.objects.print())
    # print(tiled.sets.get_set())
    # print(tiled.get_subsprites(tiled.get_id_tiles()))
