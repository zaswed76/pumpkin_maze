import json
import os

from libs import subsprite


class Layer:
    def __init__(self, layers: dict):
        super().__init__()
        self.data = layers['data']
        self.height = layers['height']
        self.name = layers['name']
        self.opacity = layers['opacity']
        self.type = layers['type']
        self.visible = layers['visible']
        self.width = layers['width']
        self.x = layers['x']
        self.y = layers['y']


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


class TiledParser:
    def __init__(self, json_map: str, tileset_dir: str):

        """
        создаёт объект карты, объект SubSprite
        :param json_map: str path каталог размещения json карты
        :param tileset_dir: str path каталог размещения tileseta
        """

        self.tileset_dir = tileset_dir
        # загрузка карты
        self.json_map = self.load_map(json_map)
        # слои
        self.layers = self.json_map['layers']
        # [0] парсится карта ТОЛЬКО с одним тайлсетом
        self.sets = TileSets(self.json_map['tilesets'][0])
        # объект SubSprite
        self.subsprite = subsprite.SubSprite(
            self.get_tileset_path(),
            self.json_map['tilewidth'],
            self.json_map['tileheight'])

    def get_tileset_path(self):
        pth = self.sets['image']
        return os.path.join(self.tileset_dir, os.path.basename(pth))

    def load_map(self, level_map: str) -> dict:
        with open(level_map, "r") as f:
            return json.load(f)

    def print_json_map(self):
        for k, v in self.json_map.items():
            print(k, v, sep=' = ')
            print('----------------------------')
        print('################')
        print('len = {}'.format(len(self.json_map)))

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
            for tile in lay['data']:
                if tile:
                    # сдвигаем на один назад (в json карте отсчёт от 1)
                    tiles.add(tile - 1)
        return tiles


if __name__ == '__main__':
    from pumpkin import paths

    pth_map = os.path.join(paths.maps, 'map1.json')
    tiled = TiledParser(pth_map, paths.tilesets)
    tiled.print_json_map()
    # print(tiled.get_tileset_path())
    # print(tiled.sets.get_set())
    # print(tiled.get_subsprites(tiled.get_id_tiles()))
