
from pumpkin2.tiledlib import abctiled


class Tiled(abctiled.AbcTiled):
    """
    класс представляет карту сгенерированую Tiled Map Editor,
    где атрибуты соответствуют ключам словаря сгенерированой карты
    """
    def __init__(self, map_dict: dict, **kwargs):
        """
         карта в виде словаря
        :param map_dict:
        :param kwargs:
        """
        super().__init__(map_dict)
        self.sets_dir = kwargs.get('sets_dir')



if __name__ == '__main__':
    from pumpkin2 import paths
    path_map = paths.get_map('level_1')
    maps = Tiled.load_map(path_map)
    sets_dir = paths.tilesets_dir
    tiled_map = Tiled(maps)
    print(tiled_map.tilesets)

