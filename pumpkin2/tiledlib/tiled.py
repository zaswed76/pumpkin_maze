
from pumpkin2.tiledlib import abctiled
from pumpkin2.tiledlib import subsprite

class TileSprite:
    def __init__(self, tilesets: abctiled.TileSets):
        self.tilesets = tilesets
        self.sprites = []

    def create_sprites(self):
        for tset in self.tilesets:
            image = tset.image
            w = tset.tilewidth
            h = tset.tileheight
            sub = subsprite.SubSprite(image, w, h)
            self.sprites.extend(sub.get_sprites())

    def __getitem__(self, key):
        """
        """
        if isinstance(key, slice):
            # noinspection PyTypeChecker
            assert key.start > 0, "!!!"
            return self.sprites[key.start - 1: key.stop - 1]
        else:
            assert key > 0, 'Index sprites list starts with 1'
            assert key <= len(self), \
                    '''Length is the list of sprites - {}'''.format(
                        len(self))
            return self.sprites[key - 1]

    def __len__(self):
        return len(self.sprites)

    def __repr__(self):
        return str(self.sprites)

class Tiled(abctiled.AbcTiled):
    """
    класс представляет карту сгенерированую Tiled Map Editor,
    где атрибуты соответствуют ключам словаря сгенерированой карты
    """
    def __init__(self, map_dict: dict, sets_dir: str, **kwargs):
        """
         карта в виде словаря
        :param sets_dir: путь к каталогу с тайлсетами
        :param map_dict:
        :param kwargs:
        """
        super().__init__(map_dict, sets_dir)
        self.sets_dir = sets_dir

    @property
    def sub_sprites(self):
        sub = TileSprite(self.tilesets)
        sub.create_sprites()
        return sub

    @property
    def size(self):
        w = self.width * self.tilewidth
        h = self.height * self.tileheight
        return (w, h)


if __name__ == '__main__':
    from pumpkin2 import paths
    path_map = paths.get_map('level_1')
    maps = Tiled.load_map(path_map)
    sets_dir = paths.exsets
    tiled_map = Tiled(maps, sets_dir)
    print(tiled_map.tilesets)

